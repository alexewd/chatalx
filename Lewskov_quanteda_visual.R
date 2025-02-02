library(quanteda)
library(quanteda.textstats)
library(progress)

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
my_stopwords <- c(stopwords("ru"), "не","на","только","с","к","я","о","а","ему","от","у","она","но","так","все","было","что","и","в","его","как","из","еще","за","это","бы","вы","то","он","же","по","ее","это", "в", "с", "и", "который", "свой", "весь", "хотя", "вообще", "ох", "всё", "ты","который","которые","ежели", "очень", "бы", "что-то", "—", "…","— "," —")

# Очистка текста и создание токенов
tokens <- tokens(corpus, 
                 remove_punct = TRUE,  # Удаление знаков препинания
                 remove_numbers = TRUE,  # Удаление чисел
                 remove_symbols = TRUE,  # Удаление символов
                 remove_separators = TRUE)  # Удаление разделителей

# Приведение токенов к нижнему регистру и удаление своих стоп-слов
tokens <- tokens_tolower(tokens)
tokens <- tokens_remove(tokens, my_stopwords)  # Удаление своих стоп-слов

# Создание документ-термин матрицы (DTM)
dtm <- dfm(tokens)

# Преобразование DTM в data.frame
term_matrix_df <- convert(dtm, to = "data.frame")

# Пример частотного анализа
term_freq <- colSums(as.matrix(dtm))
term_freq_df <- data.frame(term = names(term_freq), freq = term_freq)
term_freq_df <- term_freq_df[order(term_freq_df$freq, decreasing = TRUE), ]
top_terms <- head(term_freq_df, 20)
print(top_terms)

# Пример анализа ассоциаций терминов
# Создание DFM для термина "любовь"
term_love <- dfm_select(dtm, pattern = "любовь")

# Анализ ассоциаций
associations <- textstat_simil(dtm, y = term_love, margin = "features", method = "correlation")

# Преобразование результата в data.frame
assoc_df <- as.data.frame(as.table(as.matrix(associations)))
assoc_df <- assoc_df[order(-assoc_df$Freq), ]  # Сортировка по убыванию корреляции
colnames(assoc_df) <- c("term", "correlation")
print(assoc_df)
