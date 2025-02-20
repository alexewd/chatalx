# Загрузка необходимых библиотек
library(rvest)
library(stringr)
library(tidytext)
library(dplyr)
library(readr)
library(tidyr)

# Загрузка словаря
dict <- read_csv("https://raw.githubusercontent.com/text-machine-lab/sentimental/master/sentimental/word_list/russian.csv")

# Переименуем колонки для удобства
colnames(dict) <- c("word", "score")

# Агрегация оценок в словаре, чтобы оставить только одно значение для каждого слова
dict <- dict %>%
  group_by(word) %>%
  summarise(score = mean(score, na.rm = TRUE), .groups = 'drop')  # Используем среднее значение

# Загрузка текстов из папки
text_files <- list.files("e:/cleaned_text", full.names = TRUE)

# Создание пустого датафрейма для хранения результатов
results <- data.frame(file = character(), 
                      sentiment_score = numeric(), 
                      positive_count = integer(), 
                      negative_count = integer(), 
                      stringsAsFactors = FALSE)

# Создание пустого датафрейма для хранения найденных слов
found_words <- data.frame(positive = character(), 
                          positive_count = integer(), 
                          negative = character(), 
                          negative_count = integer(), 
                          stringsAsFactors = FALSE)

# Анализ каждого текстового файла
for (file in text_files) {
  # Чтение текста из файла
  text <- read_lines(file) %>% paste(collapse = " ")  # Объединение строк в один текст
  words <- tibble(word = unlist(str_split(text, "\\s+")))  # Разделение текста на слова
  
  # Подсчет суммарной оценки тональности и количества положительных и отрицательных слов
  sentiment_data <- words %>%
    inner_join(dict, by = "word") %>%
    mutate(sentiment = ifelse(score > 0, "positive", "negative")) %>%
    group_by(sentiment, word) %>%
    summarise(count = n(), .groups = 'drop') %>%
    ungroup()
  
  # Подсчет общего количества положительных и отрицательных слов
  sentiment_summary <- sentiment_data %>%
    group_by(sentiment) %>%
    summarise(count = sum(count), .groups = 'drop') %>%
    pivot_wider(names_from = sentiment, values_from = count, values_fill = list(count = 0))
  
  # Извлечение значений
  positive_count <- ifelse("positive" %in% colnames(sentiment_summary), sentiment_summary$positive, 0)
  negative_count <- ifelse("negative" %in% colnames(sentiment_summary), sentiment_summary$negative, 0)
  sentiment_score <- sum(sentiment_data$count * sentiment_data$score)  # Общая оценка
  
  # Добавление результатов в общий датафрейм
  results <- rbind(results, data.frame(file = basename(file), 
                                       sentiment_score = sentiment_score, 
                                       positive_count = positive_count, 
                                       negative_count = negative_count))
  
  # Создание датафреймов для положительных и отрицательных слов
  positive_words <- sentiment_data %>% filter(sentiment == "positive") %>% select(word, count)
  negative_words <- sentiment_data %>% filter(sentiment == "negative") %>% select(word, count)
  
  # Объединение положительных и отрицательных слов в один датафрейм
  combined_words <- full_join(positive_words, negative_words, by = "word", suffix = c("_positive", "_negative"))
  
  # Заполнение NA значений нулями
  combined_words[is.na(combined_words)] <- 0
  
  # Добавление найденных слов в общий датафрейм
  found_words <- rbind(found_words, combined_words)
}

# Сортировка найденных слов по убыванию count
found_words <- found_words %>%
  arrange(desc(count_positive), desc(count_negative))

# Вывод результатов
print(results)

# Вывод найденных слов
print(found_words)
tail(found_words)
