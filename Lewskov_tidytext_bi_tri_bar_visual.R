library(tidyverse)
library(tidytext)
library(stringr)
library(progress)

# Путь к каталогу с текстами
folder_path <- "e:/cleaned_text"

# Чтение всех текстов из файлов в каталоге
file_paths <- list.files(folder_path, full.names = TRUE, pattern = "\\.txt$")

# Прогресс-бар для загрузки файлов
pb_load <- progress_bar$new(total = length(file_paths), clear = FALSE, width = 100, format = "[:bar] :percent :eta")

# Создание пустого списка для всех текстов
all_texts <- c()

# Загрузка текстов из файлов
for (file_path in file_paths) {
  text_data <- read_lines(file_path, locale = locale(encoding = "UTF-8"))
  all_texts <- c(all_texts, text_data)  # Добавляем тексты в общий список
  pb_load$tick()  # Обновляем прогресс-бар для загрузки
}

# Список собственных стоп-слов
my_stopwords <- c(stopwords("ru"), "не", "на", "только", "с", "к", "я", "о", "а", "ему", "от", "у", "она", 
                  "но", "так", "все", "было", "что", "и", "в", "его", "как", "из", "еще", "за", "это", "бы", 
                  "вы", "то", "он", "же", "по", "ее", "это", "в", "с", "и", "который", "свой", "весь", "хотя", 
                  "вообще", "ох", "всё", "ты", "который", "которые", "ежели", "очень", "бы", "что-то", "—", 
                  "…", "— ", " —")

# Обработка данных
text_df <- tibble(text = all_texts)

# Очистка текста
text_df <- text_df %>%
  mutate(text = str_to_lower(text),
         text = str_remove_all(text, "[[:punct:]]"),
         text = str_remove_all(text, "[[:digit:]]"),
         text = str_remove_all(text, "[^[:alpha:][:space:]]"))

# Прогресс-бар для токенов
pb_tokens <- progress_bar$new(total = nrow(text_df), clear = FALSE, width = 100, format = "[:bar] :percent :eta")

# Разбиваем текст на токены и удаляем стоп-слова
tokens <- text_df %>%
  unnest_tokens(word, text) %>%
  anti_join(tidytext::stop_words, by = c("word" = "word")) %>%  # Убираем стандартные стоп-слова
  anti_join(tibble(word = my_stopwords), by = "word")  # Убираем свои стоп-слова

# Частотный анализ для токенов
term_freq <- tokens %>%
  count(word, sort = TRUE)

# Прогресс-бар для биграмм
pb_bigrams <- progress_bar$new(total = nrow(text_df), clear = FALSE, width = 100, format = "[:bar] :percent :eta")
bigrams <- text_df %>%
  unnest_tokens(bigram, text, token = "ngrams", n = 2) %>%
  separate(bigram, c("word1", "word2"), sep = " ") %>%
  count(word1, word2, sort = TRUE) %>%
  unite(bigram, word1, word2, sep = " ") %>%
  filter(!is.na(bigram))

# Частотный анализ для биграмм
bigram_freq <- bigrams %>%
  count(bigram, sort = TRUE)

# Прогресс-бар для триграмм
pb_trigrams <- progress_bar$new(total = nrow(text_df), clear = FALSE, width = 100, format = "[:bar] :percent :eta")
trigrams <- text_df %>%
  unnest_tokens(trigram, text, token = "ngrams", n = 3) %>%
  separate(trigram, c("word1", "word2", "word3"), sep = " ") %>%
  count(word1, word2, word3, sort = TRUE) %>%
  unite(trigram, word1, word2, word3, sep = " ") %>%
  filter(!is.na(trigram))

# Частотный анализ для триграмм
trigram_freq <- trigrams %>%
  count(trigram, sort = TRUE)

# Визуализация
wordcloud(words = term_freq$word, freq = term_freq$n, max.words = 40, colors = "darkblue", random.order = FALSE, scale = c(3, 0.5))
wordcloud(words = bigram_freq$bigram, freq = bigram_freq$n, max.words = 40, colors = "darkred", random.order = FALSE, scale = c(3, 0.5))
wordcloud(words = trigram_freq$trigram, freq = trigram_freq$n, max.words = 40, colors = "darkgreen", random.order = FALSE, scale = c(3, 0.5))
