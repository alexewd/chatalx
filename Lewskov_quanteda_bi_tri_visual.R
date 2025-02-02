library(quanteda)
library(quanteda.textstats)
library(progress)
library(wordcloud)

# Путь к каталогу с текстами
folder_path <- "e:/cleaned_text"

# Получение списка всех файлов с расширением .txt в папке
file_paths <- list.files(path = folder_path, pattern = "\\.txt$", full.names = TRUE)

# Создание пустого списка для хранения текстов
all_texts <- character()

# Прогресс-бар для отслеживания загрузки
pb <- progress_bar$new(total = length(file_paths), clear = FALSE, width = 100, format = "[:bar] :percent :eta")

# Чтение всех текстов из файлов
for (file_path in file_paths) {
  text_data <- readLines(file_path, encoding = "UTF-8")
  all_texts <- c(all_texts, text_data)  # Добавляем тексты в общий список
  pb$tick()  # Обновляем прогресс-бар
}

# Создание корпуса текста с использованием quanteda
corpus <- corpus(all_texts)

# Создание списка своих стоп-слов
my_stopwords <- c(stopwords("ru"), "не","на","только","с","к","я","о","а","ему","от","у","она","но","так","все","было","что","и","в","его","как","из","еще","за","это","бы","вы","то","он","же","по","ее","это", "г", "с", "и", "который", "свой", "весь", "хотя", "вообще", "ох", "всё", "ты","который","которые","ежели", "очень", "бы", "что-то", "—", "…","— "," —","_","ирли","см")

# Очистка текста и создание токенов
tokens <- tokens(corpus, 
                 remove_punct = TRUE,  # Удаление знаков препинания
                 remove_numbers = TRUE,  # Удаление чисел
                 remove_symbols = TRUE,  # Удаление символов
                 remove_separators = TRUE)  # Удаление разделителей

# Приведение токенов к нижнему регистру и удаление своих стоп-слов
tokens <- tokens_tolower(tokens)
tokens <- tokens_remove(tokens, my_stopwords)  # Удаление своих стоп-слов

# Создание разреженной документ-термин матрицы (DTM)
dtm <- dfm(tokens)

# Частотный анализ для монограмм
term_freq <- textstat_frequency(dtm)  # Частотный анализ для разреженной матрицы
top_terms <- head(term_freq, 20)  # Топ-20 самых частых терминов
print(top_terms)
smpl_terms <- sample_n(term_freq, 20)  # Топ-20 самых частых терминов
print(smpl_terms)
# Визуализация монограмм с использованием wordcloud
wordcloud(words = term_freq$feature, freq = term_freq$frequency, max.words = 40, 
          colors = "darkblue", random.order = FALSE, scale = c(3, 0.5))

# Создание биграмм
bigrams <- tokens_ngrams(tokens, n = 2)

# Создание разреженной матрицы для биграмм
dtm_bigrams <- dfm(bigrams)

# Частотный анализ для биграмм
bigram_freq <- textstat_frequency(dtm_bigrams)

top_bigrams <- head(bigram_freq, 20)

# Убираем подчёркивания в биграммах
top_bigrams$feature <- str_replace_all(top_bigrams$feature, "_", " ")

# Выводим отформатированный результат
print(top_bigrams)

smpl_bigrams <- sample_n(bigram_freq, 20)

# Убираем подчёркивания в биграммах
smpl_bigrams$feature <- str_replace_all(smpl_bigrams$feature, "_", " ")

print(smpl_bigrams)

top_bigrams$feature <- str_replace_all(top_bigrams$feature, "_", " ")
top_bi_feature <- top_bigrams$feature
# Визуализация биграмм с использованием wordcloud
wordcloud(words = top_bi_feature, freq = bigram_freq$frequency, max.words = 40, 
          colors = "darkred", random.order = FALSE, scale = c(3, 0.5))

# Создание триграмм
trigrams <- tokens_ngrams(tokens, n = 3)

# Создание разреженной матрицы для триграмм
dtm_trigrams <- dfm(trigrams)

# Частотный анализ для триграмм
trigram_freq <- textstat_frequency(dtm_trigrams)
top_trigrams <- head(trigram_freq, 20)
top_trigrams$feature <- str_replace_all(top_trigrams$feature, "_", " ")
print(top_trigrams)
smpl_trigrams <- sample_n(trigram_freq, 20)
smpl_trigrams$feature <- str_replace_all(smpl_trigrams$feature, "_", " ")
print(smpl_trigrams)

# Визуализация триграмм с использованием wordcloud
top_trigrams$feature <- str_replace_all(top_trigrams$feature, "_", " ")
top_tri_feature <- top_trigrams$feature

wordcloud(words = top_tri_feature, freq = trigram_freq$frequency, max.words = 40, 
          colors = "darkgreen", random.order = FALSE, scale = c(3, 0.5))
