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
my_stopwords <- c(stopwords("ru"),"а","то", "все", "она", "так", "его", "но", "да", "ты", "к", "у", "же", "вы", "за","со", "как", "н", "то", "г","нет", "о", "из", "ему", "теперь","был", "него", "до", "вас",
"бы", "по", "только", "ее", "мне", "было", "вот", "от", "меня", "еще", "они",
"когда", "даже", "ну", "вдруг", "ли", "если", "уже", "или", "ни", "быть", 
 "нибудь", "опять", "уж", "вам", "ведь", "там", "потом", "себя", "ничего", "ей", "может", 
"тут", "где", "есть", "надо", "ней", "для", "мы", "тебя", "их", "чем", "была", "сам", "чтоб", 
"без", "будто", "чего", "раз", "тоже", "себе", "под", "жизнь", "будет", "ж", "тогда", "кто",
"этот", "говорил", "того", "потому", "этого", "какой", "совсем", "ним", "здесь", "этом",
"один", "почти", "мой", "тем", "чтобы", "нее", "кажется", "сейчас", "были", "куда",
"зачем", "сказать", "всех", "никогда", "сегодня", "можно", "при", "наконец", "два",
"об", "другой", "хоть", "после", "над", "больше", "тот", "через", "эти", "нас", "про",
"них", "какая", "много", "разве", "три", "эту", "моя", "впрочем", "хорошо", "свою",
"этой", "перед", "иногда", "лучше", "чуть", "том", "нельзя", "такой", "им", "более",
"всегда", "конечно", "всю", "между","это", "сказал", "сказала",
"пьер","сказал", "то", ",","не", "что", "он", "на", "я", "с")


# Обработка данных
text_df <- tibble(text = all_texts)

# Очистка текста
text_df <- text_df %>%
  mutate(text = str_to_lower(text),
         text = str_remove_all(text, "[[:punct:]]"),
         text = str_remove_all(text, "[[:digit:]]"),
         text = str_remove_all(text, "[^[:alpha:][:space:]]"))  # Убираем все символы, кроме букв и пробелов

# Разбиваем текст на токены и удаляем стоп-слова
tokens <- text_df %>%
  unnest_tokens(word, text) %>%
  anti_join(tidytext::stop_words, by = c("word" = "word")) %>%  # Убираем стандартные стоп-слова
  anti_join(tibble(word = my_stopwords), by = "word") %>%  # Убираем свои стоп-слова
  filter(str_detect(word, "^[а-яА-Я]+$")) %>%  # Убираем все латинские буквы и символы
  filter(!is.na(word))  # Убираем NA

# Частотный анализ для монограмм
monogram_freq <- tokens %>%
  count(word, sort = TRUE)

# Вывод первых 20 монограмм
print(head(monogram_freq, 20))

# Биграммы
bigrams <- text_df %>%
  unnest_tokens(bigram, text, token = "ngrams", n = 2) %>%
  separate(bigram, c("word1", "word2"), sep = " ") %>%
  count(word1, word2, sort = TRUE) %>%
  unite(bigram, word1, word2, sep = " ") %>%
  filter(!is.na(bigram)) %>%
  filter(str_detect(bigram, "^[а-яА-Я ]+$"))  # Убираем биграммы с латинскими буквами

# Частотный анализ для биграмм
bigram_freq <- bigrams %>%
  count(bigram, sort = TRUE)

# Вывод первых 20 биграмм
print(head(bigram_freq, 20))
print(sample_n(bigram_freq, 20))
# Триграммы
trigrams <- text_df %>%
  unnest_tokens(trigram, text, token = "ngrams", n = 3) %>%
  separate(trigram, c("word1", "word2", "word3"), sep = " ") %>%
  count(word1, word2, word3, sort = TRUE) %>%
  unite(trigram, word1, word2, word3, sep = " ") %>%
  filter(!is.na(trigram)) %>%
  filter(str_detect(trigram, "^[а-яА-Я ]+$"))  # Убираем триграммы с латинскими буквами

# Частотный анализ для триграмм
trigram_freq <- trigrams %>%
  count(trigram, sort = TRUE)

# Вывод первых 20 триграмм
print(head(trigram_freq, 20))
print(sample_n(trigram_freq, 20))
# Визуализация
wordcloud(words = monogram_freq$word, freq = monogram_freq$n, max.words = 40, colors = "darkblue", random.order = FALSE, scale = c(3, 0.5))
wordcloud(words = bigram_freq$bigram, freq = bigram_freq$n, max.words = 40, colors = "darkred", random.order = FALSE, scale = c(3, 0.5))
wordcloud(words = trigram_freq$trigram, freq = trigram_freq$n, max.words = 40, colors = "darkgreen", random.order = FALSE, scale = c(3, 0.5))
