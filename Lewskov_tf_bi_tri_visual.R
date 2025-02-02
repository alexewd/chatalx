library(tm)
library(tidytext)
library(dplyr)
library(stringr)
library(stopwords)
library(ggplot2)
library(wordcloud)
library(wordcloud2)
# Функция для загрузки текстов из папки
load_texts_from_folder <- function(folder_path) {
  file_paths <- list.files(folder_path, pattern = "\\.txt$", full.names = TRUE)  # Чтение всех текстов с расширением .txt
  texts <- lapply(file_paths, function(file) {
    readLines(file, warn = FALSE) %>% paste(collapse = "\n")
  })
  return(texts)
}

# Указываем путь к папке с текстами Н. С. Лескова
folder_path <- "e:/cleaned_text"  # Путь к папке, где находятся файлы

# Загружаем все тексты
texts <- load_texts_from_folder(folder_path)

# Добавляем стоп-слова, включая русские
stop_words_ru <- stopwords("ru")  # Русские стоп-слова
# Добавляем свои стоп-слова (если есть)
custom_stopwords <- c("а","то", "все", "она", "так", "его", "но", "да", "ты", "к", "у", "же", "вы", "за","со", "как", "н", "то", "г","нет", "о", "из", "ему", "теперь","был", "него", "до", "вас",
"бы", "по", "только", "ее", "мне", "было", "вот", "от", "меня", "еще", "они",
"когда", "даже", "ну", "вдруг", "ли", "если", "уже", "или", "ни", "быть", 
"нибудь", "опять", "уж", "вам", "ведь", "там", "потом", "себя", "ничего", "ей", "может",                  "тут", "где", "есть", "надо", "ней", "для", "мы", "тебя", "их", "чем", "была", "сам", "чтоб", 
"без", "будто", "чего", "раз", "тоже", "себе", "под", "жизнь", "будет", "ж", "тогда", "кто",
"этот", "говорил", "того", "потому", "этого", "какой", "совсем", "ним", "здесь", "этом",
"один", "почти", "мой", "тем", "чтобы", "нее", "кажется", "сейчас", "были", "куда",
"зачем", "сказать", "всех", "никогда", "сегодня", "можно", "при", "наконец", "два",
"об", "другой", "хоть", "после", "над", "больше", "тот", "через", "эти", "нас", "про",
"них", "какая", "много", "разве", "три", "эту", "моя", "впрочем", "хорошо", "свою",
"этой", "перед", "иногда", "лучше", "чуть", "том", "нельзя", "такой", "им", "более",
"всегда", "конечно", "всю", "между","это", "сказал", "сказала",
"то", ",","не", "что", "он", "на", "я", "с")  # Укажите свои стоп-слова
stop_words <- c(stop_words_ru, custom_stopwords)

# Преобразуем тексты в data.frame
texts_df <- tibble(text = texts)

# Разбиваем тексты на токены, удаляем стоп-слова и извлекаем нграммы (монограммы, биграммы, триграммы)
ngram_df <- texts_df %>%
  unnest_tokens(word, text) %>%
  filter(!word %in% stop_words)  # Убираем стоп-слова

# Извлекаем монограммы
monogram_df <- ngram_df %>%
  count(word, sort = TRUE)

# Извлекаем биграммы
bigram_df <- texts_df %>%
  unnest_tokens(bigram, text, token = "ngrams", n = 2) %>%
  count(bigram, sort = TRUE)

# Извлекаем триграммы
trigram_df <- texts_df %>%
  unnest_tokens(trigram, text, token = "ngrams", n = 3) %>%
  count(trigram, sort = TRUE)

# Выбираем топ-10 для монограмм, биграмм и триграмм
top_monograms <- monogram_df %>%
  top_n(20, n)

top_bigrams <- bigram_df %>%
  top_n(20, n)

top_trigrams <- trigram_df %>%
  top_n(20, n)

# Печатаем топ-10 монограмм, биграмм и триграмм
cat("Топ-10 монограмм:\n")
print(top_monograms)

cat("\nТоп-10 биграмм:\n")
print(top_bigrams)

cat("\nТоп-10 триграмм:\n")
print(top_trigrams)

# Визуализируем монограммы
ggplot(top_monograms, aes(x = reorder(word, n), y = n)) +
  geom_bar(stat = "identity", fill = "steelblue") +
  labs(title = "Топ-10 монограмм", x = "Монограмма", y = "Частота") +
  coord_flip()
# 
# Создаем облако слов для монограмм с ограничением до 100 слов
wordcloud(words = monogram_df$word, freq = monogram_df$n, min.freq = 1, 
          scale = c(3, 0.5), colors = brewer.pal(8, "Dark2"), 
          max.words = 100, random.order = FALSE, rot.per = 0.25)
