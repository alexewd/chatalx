# Установка необходимых пакетов (раскомментируйте, если пакеты не установлены)
# if (!require("quanteda")) {
#   install.packages("quanteda", lib = "C:/Users/<Username>/Documents/R/win-library/4.4")
# }
# if (!require("data.table")) {
#   install.packages("data.table", lib = "C:/Users/<Username>/Documents/R/win-library/4.4")
# }
# if (!require("stopwords")) {
#   install.packages("stopwords", lib = "C:/Users/<Username>/Documents/R/win-library/4.4")
# }
# if (!require("stringr")) {
#   install.packages("stringr", lib = "C:/Users/<Username>/Documents/R/win-library/4.4")
# }
# if (!require("parallel")) {
#   install.packages("parallel", lib = "C:/Users/<Username>/Documents/R/win-library/4.4")
# }
# if (!require("udpipe")) {
#   install.packages("udpipe", lib = "C:/Users/<Username>/Documents/R/win-library/4.4")
# }
# if (!require("wordcloud")) {
#   install.packages("wordcloud", lib = "C:/Users/<Username>/Documents/R/win-library/4.4")
# }
# if (!require("ggplot2")) {
#   install.packages("ggplot2", lib = "C:/Users/<Username>/Documents/R/win-library/4.4")
# }

# Загрузка библиотек
library(quanteda)
library(data.table)
library(stopwords)
library(stringr)
library(parallel)
library(udpipe)
library(wordcloud)
library(ggplot2)

# Настройка путей библиотек (раскомментируйте, если нужно)
# .libPaths(c("C:/Users/<Username>/Documents/R/win-library/4.4", .libPaths()))

# Оптимизация quanteda для многопоточности
quanteda_options(threads = detectCores() - 1)

# 1. Чтение текста
text_file <- "D:/NLP_Toxic/WP/oblomov.txt"
if (!file.exists(text_file)) stop("Файл не найден!")
text_lines <- readLines(text_file, encoding = "UTF-8", warn = FALSE)
text <- paste(text_lines, collapse = " ")
corpus <- corpus(text)

# 2. Статистика по знакам пунктуации и не буквенным знакам
punct_tokens <- tokens(text, what = "character")
punct_tokens <- punct_tokens[[1]][!grepl("[[:alpha:]]|[[:digit:]]", punct_tokens[[1]])]
punct_freq <- table(punct_tokens)
punct_table <- data.table(
  Symbol = names(punct_freq),
  Frequency = as.integer(punct_freq)
)[order(-Frequency)]
print("Таблица частоты знаков пунктуации и не буквенных символов:")
print(punct_table)

# 3. Статистика по цифрам с примерами предложений
sentences <- tokens(text, what = "sentence")
sentences <- as.character(unlist(sentences))
number_matches <- str_extract_all(sentences, "\\d")
number_freq <- table(unlist(number_matches))
number_table <- data.table(
  Number = names(number_freq),
  Frequency = as.integer(number_freq),
  Example_Sentence = character(length(number_freq))
)
for (num in number_table$Number) {
  sentence_with_num <- sentences[str_detect(sentences, num)][1]
  number_table[Number == num, Example_Sentence := ifelse(is.na(sentence_with_num), "Нет примера", sentence_with_num)]
}
print("Таблица частоты цифр с примерами предложений:")
print(number_table)

# 4. Таблица глав (римские цифры и первые предложения)
roman_pattern <- "^\\s*(I{1,3}|IV|VI{0,3}|X{1,3})\\s*\\.?\\s*$"  # Улучшенное выражение для I-XII
chapter_starts <- which(str_detect(text_lines, roman_pattern))

# Диагностика: проверяем, найдены ли строки с римскими цифрами
if (length(chapter_starts) == 0) {
  cat("Римские цифры не найдены. Пример строк текста:\n")
  print(head(text_lines, 10))  # Выводим первые 10 строк для проверки
  stop("Проверьте формат глав в файле.")
}

chapter_table <- data.table(
  Chapter = character(),
  First_Sentence = character()
)

for (i in seq_along(chapter_starts)) {
  chapter_num <- str_extract(text_lines[chapter_starts[i]], roman_pattern)
  # Находим следующую строку с текстом (пропуская пустые строки)
  next_line_idx <- chapter_starts[i] + 1
  while (next_line_idx <= length(text_lines) && 
         str_trim(text_lines[next_line_idx]) == "") {
    next_line_idx <- next_line_idx + 1
  }
  if (next_line_idx > length(text_lines)) next_line_idx <- chapter_starts[i]
  
  # Собираем текст начиная с этой строки
  next_lines <- text_lines[next_line_idx:length(text_lines)]
  next_text <- paste(next_lines, collapse = " ")
  first_sentence <- as.character(unlist(tokens(next_text, what = "sentence")))[1]
  
  chapter_table <- rbind(chapter_table, data.table(
    Chapter = str_trim(chapter_num),
    First_Sentence = ifelse(is.na(first_sentence), "Нет предложения", first_sentence)
  ))
}

print("Таблица глав и первых предложений:")
print(chapter_table)

# 5. Имена собственные/ФИО
udmodel <- udpipe_download_model(language = "russian")
udmodel <- udpipe_load_model(udmodel$file_model)
annotated <- udpipe_annotate(udmodel, x = text, tagger = "default", parser = "none")
annotated_dt <- as.data.table(annotated)
proper_nouns <- annotated_dt[upos == "PROPN", .(Token = token)]
# Исключаем нежелательные имена собственные
unwanted_proper <- c("Ну", "Да")  # Добавьте сюда слова, которые не являются именами
proper_nouns <- proper_nouns[!Token %in% unwanted_proper]
# Фильтруем имена короче 3 символов
proper_nouns <- proper_nouns[nchar(Token) >= 3]
proper_noun_freq <- proper_nouns[, .(Frequency = .N), by = Token][order(-Frequency)]
print("Таблица имён собственных/ФИО:")
print(proper_noun_freq)

# 6. Слова на латинице
latin_words <- str_extract_all(text, "\\b[a-zA-Z]+\\b")[[1]]
latin_freq <- table(latin_words)
latin_table <- data.table(
  Latin_Word = names(latin_freq),
  Frequency = as.integer(latin_freq)
)[order(-Frequency)]
print("Таблица слов на латинице:")
print(latin_table)

# Пользовательский список стоп-слов
custom_stopwords <- c("ну", "да", "б", "а", "в", "г")  # Добавляйте свои стоп-слова сюда

# 7. Частота слов (без стоп-слов, имен собственных, пользовательских стоп-слов и коротких слов)
tokens_clean <- tokens(corpus, 
                       remove_punct = TRUE, 
                       remove_numbers = TRUE, 
                       remove_symbols = TRUE, 
                       remove_separators = TRUE)
tokens_clean <- tokens_tolower(tokens_clean)

# Объединяем стандартные стоп-слова с пользовательскими
russian_stopwords <- stopwords("ru", source = "stopwords-iso")
all_stopwords <- unique(c(russian_stopwords, custom_stopwords))
tokens_clean <- tokens_remove(tokens_clean, all_stopwords)

# Удаляем имена собственные
proper_nouns_list <- tolower(proper_nouns$Token)  # Приводим к нижнему регистру
tokens_clean <- tokens_remove(tokens_clean, proper_nouns_list)

# Удаляем слова короче 2 символов
tokens_clean <- tokens_select(tokens_clean, min_nchar = 2)

dfm_words <- dfm(tokens_clean)
word_freq <- colSums(dfm_words)
word_table <- data.table(
  Word = names(word_freq),
  Frequency = as.integer(word_freq)
)[order(-Frequency)]
print("Таблица частоты слов (без стоп-слов, имен собственных, пользовательских стоп-слов и коротких слов):")
print(word_table)

# 8. Биграммы
tokens_ngrams <- tokens_ngrams(tokens_clean, n = 2)
dfm_bigrams <- dfm(tokens_ngrams)
bigram_freq <- colSums(dfm_bigrams)
bigram_table <- data.table(
  Bigram = names(bigram_freq),
  Frequency = as.integer(bigram_freq)
)[order(-Frequency)]
print("Таблица частоты биграмм:")
print(bigram_table)

# 9. Триграммы
tokens_trigrams <- tokens_ngrams(tokens_clean, n = 3)
dfm_trigrams <- dfm(tokens_trigrams)
trigram_freq <- colSums(dfm_trigrams)
trigram_table <- data.table(
  Trigram = names(trigram_freq),
  Frequency = as.integer(trigram_freq)
)[order(-Frequency)]
print("Таблица частоты триграмм:")
print(trigram_table)

# 10. Средняя длина предложений
sentence_tokens <- tokens(corpus, what = "sentence")
sentence_lengths <- sapply(sentence_tokens, function(s) {
  length(tokens(s, remove_punct = TRUE, remove_numbers = TRUE, remove_symbols = TRUE)[[1]])
})
mean_sentence_length <- mean(sentence_lengths, na.rm = TRUE)
cat("Средняя длина предложений (в словах):", round(mean_sentence_length, 2), "\n")

# 12. Распределение частей речи
pos_counts <- annotated_dt[, .(Count = .N), by = upos]
total_tokens <- nrow(annotated_dt)
pos_counts[, Proportion := Count / total_tokens]
pos_counts <- pos_counts[order(-Count)]
print("Распределение частей речи:")
print(pos_counts)

# Сохранение результатов в CSV
fwrite(pos_counts, "pos_distribution.csv")
print("Таблица распределения частей речи сохранена в pos_distribution.csv")


# 11. Визуализации
# Wordcloud для слов
set.seed(123)  # Для воспроизводимости
wordcloud(words = word_table$Word, freq = word_table$Frequency, 
          max.words = 100, random.order = FALSE, 
          colors = brewer.pal(8, "Dark2"))
png("wordcloud.png", width = 800, height = 600)
wordcloud(words = word_table$Word, freq = word_table$Frequency, 
          max.words = 100, random.order = FALSE, 
          colors = brewer.pal(8, "Dark2"))
dev.off()
print("Облако слов сохранено в wordcloud.png")

# Гистограмма для пунктуации (топ-10)
punct_top <- head(punct_table, 10)
p1 <- ggplot(punct_top, aes(x = reorder(Symbol, -Frequency), y = Frequency)) +
  geom_bar(stat = "identity", fill = "steelblue") +
  labs(title = "Частота знаков пунктуации (Топ-10)", x = "Знак", y = "Частота") +
  theme_minimal()
print(p1)  # Вывод на экран
ggsave("punctuation_plot.png", p1, width = 8, height = 6)
print("Гистограмма пунктуации сохранена в punctuation_plot.png")

# Гистограмма для цифр
p2 <- ggplot(number_table, aes(x = Number, y = Frequency)) +
  geom_bar(stat = "identity", fill = "darkgreen") +
  labs(title = "Частота цифр", x = "Цифра", y = "Частота") +
  theme_minimal()
print(p2)  # Вывод на экран
ggsave("numbers_plot.png", p2, width = 8, height = 6)
print("Гистограмма цифр сохранена в numbers_plot.png")

# Гистограмма для имён собственных (топ-10)
proper_top <- head(proper_noun_freq, 10)
p3 <- ggplot(proper_top, aes(x = reorder(Token, -Frequency), y = Frequency)) +
  geom_bar(stat = "identity", fill = "purple") +
  labs(title = "Частота имён собственных (Топ-10)", x = "Имя", y = "Частота") +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))
print(p3)  # Вывод на экран
ggsave("proper_nouns_plot.png", p3, width = 8, height = 6)
print("Гистограмма имён собственных сохранена в proper_nouns_plot.png")

# Гистограмма для слов на латинице (если есть)
if (nrow(latin_table) > 0) {
  latin_top <- head(latin_table, 10)
  p4 <- ggplot(latin_top, aes(x = reorder(Latin_Word, -Frequency), y = Frequency)) +
    geom_bar(stat = "identity", fill = "orange") +
    labs(title = "Частота слов на латинице (Топ-10)", x = "Слово", y = "Частота") +
    theme_minimal() +
    theme(axis.text.x = element_text(angle = 45, hjust = 1))
  print(p4)  # Вывод на экран
  ggsave("latin_words_plot.png", p4, width = 8, height = 6)
  print("Гистограмма слов на латинице сохранена в latin_words_plot.png")
} else {
  cat("Нет слов на латинице для визуализации.\n")
}

# Гистограмма для слов (топ-20)
word_top <- head(word_table, 20)
p5 <- ggplot(word_top, aes(x = reorder(Word, -Frequency), y = Frequency)) +
  geom_bar(stat = "identity", fill = "red") +
  labs(title = "Частота слов (Топ-20)", x = "Слово", y = "Частота") +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))
print(p5)  # Вывод на экран
ggsave("word_freq_plot.png", p5, width = 8, height = 6)
print("Гистограмма слов сохранена в word_freq_plot.png")

# Гистограмма для биграмм (топ-10)
bigram_top <- head(bigram_table, 10)
p6 <- ggplot(bigram_top, aes(x = reorder(Bigram, -Frequency), y = Frequency)) +
  geom_bar(stat = "identity", fill = "blue") +
  labs(title = "Частота биграмм (Топ-10)", x = "Биграмма", y = "Частота") +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))
print(p6)  # Вывод на экран
ggsave("bigram_freq_plot.png", p6, width = 8, height = 6)
print("Гистограмма биграмм сохранена в bigram_freq_plot.png")

# Гистограмма для триграмм (топ-10)
trigram_top <- head(trigram_table, 10)
p7 <- ggplot(trigram_top, aes(x = reorder(Trigram, -Frequency), y = Frequency)) +
  geom_bar(stat = "identity", fill = "darkred") +
  labs(title = "Частота триграмм (Топ-10)", x = "Триграмма", y = "Частота") +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))
print(p7)  # Вывод на экран
ggsave("trigram_freq_plot.png", p7, width = 8, height = 6)
print("Гистограмма триграмм сохранена в trigram_freq_plot.png")

# Гистограмма для распределения частей речи
p8 <- ggplot(pos_counts, aes(x = reorder(upos, -Count), y = Count)) +
  geom_bar(stat = "identity", fill = "darkblue") +
  labs(title = "Распределение частей речи", x = "Часть речи", y = "Частота") +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))
print(p8)  # Вывод на экран
ggsave("pos_distribution_plot.png", p8, width = 8, height = 6)
print("Гистограмма распределения частей речи сохранена в pos_distribution_plot.png")

# Сохранение результатов в CSV
fwrite(punct_table, "punctuation_stats.csv")
fwrite(number_table, "number_stats.csv")
fwrite(chapter_table, "chapter_stats.csv")
fwrite(proper_noun_freq, "proper_nouns.csv")
fwrite(latin_table, "latin_words.csv")
fwrite(word_table, "word_freq.csv")
fwrite(bigram_table, "bigram_freq.csv")
fwrite(trigram_table, "trigram_freq.csv")
fwrite(pos_counts, "pos_distribution.csv")
write.csv(data.frame(Mean_Sentence_Length = mean_sentence_length), "sentence_length.csv")
