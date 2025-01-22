from natasha import Segmenter, MorphVocab, NewsMorphTagger, NewsEmbedding, Doc
from gensim.models import Word2Vec
import os
from pathlib import Path
import re

# Путь к папке с текстами
folder_path = Path("e:/cleaned_text")

# Инициализация компонентов Natasha
segmenter = Segmenter()
morph_vocab = MorphVocab()
embeddings = NewsEmbedding()
morph_tagger = NewsMorphTagger(embeddings)

# Функция для лемматизации текста с разбиением на предложения
def lemmatize_texts_to_sentences(texts):
    lemmatized_sentences = []
    for text in texts:
        doc = Doc(text)
        doc.segment(segmenter)
        doc.tag_morph(morph_tagger)
        for token in doc.tokens:
            token.lemmatize(morph_vocab)
        sentences = [
            " ".join([token.lemma for token in sentence.tokens if token.pos != "PUNCT"])
            for sentence in doc.sents
        ]
        lemmatized_sentences.extend(sentences)
    return lemmatized_sentences

# Загрузка текстов из папки
def load_texts_from_folder(folder_path):
    texts = []
    for file_path in folder_path.glob("*.txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
            # Убираем лишние символы
            text = re.sub(r"\s+", " ", text)
            texts.append(text)
    return texts

# Основной процесс
texts = load_texts_from_folder(folder_path)
lemmatized_sentences = lemmatize_texts_to_sentences(texts)

# Обучение модели Word2Vec
w2v_model = Word2Vec(
    sentences=[sentence.split() for sentence in lemmatized_sentences],
    vector_size=100,  # Размерность эмбеддингов
    window=5,  # Контекстное окно
    min_count=2,  # Минимальная частота слова
    workers=4,  # Количество потоков
    sg=1,  # Используем Skip-Gram (1 — Skip-Gram, 0 — CBOW)
)

# Пример: находим похожие слова
similar_words = w2v_model.wv.most_similar("человек", topn=10)

# Вывод результатов
print("Слова, похожие на 'человек':")
for word, similarity in similar_words:
    print(f"{word}: {similarity:.4f}")
