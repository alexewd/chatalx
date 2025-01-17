import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# Загрузка данных частотности
file_path = 'e:\\posl\\data\\frequencies_result.csv'
data = pd.read_csv(file_path, sep=';')

# Предобработка данных
# Убираем строки с пропущенными значениями
data = data.dropna()

# Преобразование текстового столбца 'index' в TF-IDF
vectorizer = TfidfVectorizer(max_features=100)  # Ограничиваем до 100 признаков
X_text = vectorizer.fit_transform(data['index']).toarray()

# Преобразование числовых столбцов
X_numeric = data[["File1_Word_Frequency", "File1_Bigram_Frequency", "File2_Word_Frequency", "File2_Bigram_Frequency"]]

# Объединение текстовых и числовых признаков
X_combined = np.hstack((X_text, X_numeric.values))

# Создание целевой переменной (метки классов)
y = (X_numeric["File1_Word_Frequency"] > X_numeric["File2_Word_Frequency"]).astype(int)  # Метка: 1, если чаще в первом файле

# Разделение данных на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X_combined, y, test_size=0.3, random_state=42, stratify=y)

# Обучение модели логистической регрессии
log_reg = LogisticRegression(max_iter=200, random_state=42)
log_reg.fit(X_train, y_train)
y_pred = log_reg.predict(X_test)

# Оценка модели
accuracy = accuracy_score(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)
class_report = classification_report(y_test, y_pred)

print(f"Accuracy (Logistic Regression with TF-IDF): {accuracy:.2f}")
print("Confusion Matrix:")
print(conf_matrix)
print("Classification Report:")
print(class_report)

