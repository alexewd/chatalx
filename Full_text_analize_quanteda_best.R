# Установка необходимых пакетов (если отсутствуют в package_list.csv)
# Устанавливаем в пользовательскую папку, как обсуждали
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

# Загрузка библиотек
library(quanteda)
library(data.table)
library(stopwords)
library(stringr)

# Настройка путей библиотек (для вашей конфигурации)
# .libPaths(c("C:/Users/<Username>/Documents/R/win-library/4.4", .libPaths()))

# Оптимизация quanteda для многопоточности
quanteda_options(threads = detectCores() - 1)

# 1. Чтение текста
text_file <- "D:/NLP_Toxic/WP/oblomov.txt"
if (!file.exists(text_file)) stop("Файл не найден!")
text <- readLines(text_file, encoding = "UTF-8", warn = FALSE)
text <- paste(text, collapse = " ")  # Объединяем в одну строку

# Создаём корпус
corpus <- corpus(text)

# 2. Статистика по знакам пунктуации и не буквенным знакам
# Извлекаем все знаки пунктуации и не буквенные символы
punct_tokens <- tokens(text, what = "character", remove_letters = TRUE, remove_numbers = TRUE)
punct_freq <- table(unlist(punct_tokens))
punct_table <- data.table(
  Symbol = names(punct_freq),
  Frequency = as.integer(punct_freq)
)[order(-Frequency)]
print("Таблица частоты знаков пунктуации и не буквенных символов:")
print(punct_table)

# 3. Статистика по цифрам с примерами предложений
# Токенизация по предложениям
sentences <- tokens(text, what = "sentence")
sentences <- as.character(unlist(sentences))

# Извлекаем цифры
number_matches <- str_extract_all(sentences, "\\d")
number_freq <- table(unlist(number_matches))
number_table <- data.table(
  Number = names(number_freq),
  Frequency = as.integer(number_freq),
  Example_Sentence = character(length(number_freq))
)

# Добавляем пример предложения для каждой цифры
for (num in number_table$Number) {
  sentence_with_num <- sentences[str_detect(sentences, num)][1]
  number_table[Number == num, Example_Sentence := sentence_with_num]
}
print("Таблица частоты цифр с примерами предложений:")
print(number_table)

# 4. Очистка текста и частота слов
# Токенизация слов с удалением пунктуации, цифр, символов
tokens_clean <- tokens(corpus, 
                       remove_punct = TRUE, 
                       remove_numbers = TRUE, 
                       remove_symbols = TRUE, 
                       remove_separators = TRUE)
tokens_clean <- tokens_tolower(tokens_clean)  # Приводим к нижнему регистру

# Удаляем русские стоп-слова
russian_stopwords <- stopwords("ru", source = "stopwords-iso")
tokens_clean <- tokens_remove(tokens_clean, russian_stopwords)

# Создаём Document-Term Matrix и подсчитываем частоту слов
dfm_words <- dfm(tokens_clean)
word_freq <- colSums(dfm_words)
word_table <- data.table(
  Word = names(word_freq),
  Frequency = as.integer(word_freq)
)[order(-Frequency)]
print("Таблица частоты слов (без стоп-слов):")
print(word_table)

# 5. Биграммы
tokens_ngrams <- tokens_ngrams(tokens_clean, n = 2)
dfm_bigrams <- dfm(tokens_ngrams)
bigram_freq <- colSums(dfm_bigrams)
bigram_table <- data.table(
  Bigram = names(bigram_freq),
  Frequency = as.integer(bigram_freq)
)[order(-Frequency)]
print("Таблица частоты биграмм:")
print(bigram_table)

# 6. Триграммы
tokens_trigrams <- tokens_ngrams(tokens_clean, n = 3)
dfm_trigrams <- dfm(tokens_trigrams)
trigram_freq <- colSums(dfm_trigrams)
trigram_table <- data.table(
  Trigram = names(trigram_freq),
  Frequency = as.integer(trigram_freq)
)[order(-Frequency)]
print("Таблица частоты триграмм:")
print(trigram_table)

# 7. Средняя длина предложений
# Подсчитываем количество слов в каждом предложении
sentence_tokens <- tokens(corpus, what = "sentence")
sentence_lengths <- sapply(sentence_tokens, function(s) {
  length(tokens(s, remove_punct = TRUE, remove_numbers = TRUE, remove_symbols = TRUE)[[1]])
})
mean_sentence_length <- mean(sentence_lengths, na.rm = TRUE)
cat("Средняя длина предложений (в словах):", round(mean_sentence_length, 2), "\n")

# Сохранение результатов в CSV (опционально)
fwrite(punct_table, "punctuation_stats.csv")
fwrite(number_table, "number_stats.csv")
fwrite(word_table, "word_freq.csv")
fwrite(bigram_table, "bigram_freq.csv")
fwrite(trigram_table, "trigram_freq.csv")
write.csv(data.frame(Mean_Sentence_Length = mean_sentence_length), "sentence_length.csv")
