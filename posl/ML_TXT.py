import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.decomposition import PCA
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.utils import resample
from scipy.stats import ttest_ind

# Загрузка данных частотности
file_path = 'e:\\posl\\data\\frequencies_result.csv'
data = pd.read_csv(file_path, sep=';')

# Предобработка данных
# Убираем строку с некорректными значениями, если она есть
data = data.dropna()

# Выделяем признаки (X) и целевую переменную (y)
X = data[["File1_Word_Frequency", "File1_Bigram_Frequency", "File2_Word_Frequency", "File2_Bigram_Frequency"]]
y = (X["File1_Word_Frequency"] > X["File2_Word_Frequency"]).astype(int)  # Метка: 1, если чаще в первом файле

# Разделение данных на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

# 1. Логистическая регрессия
log_reg = LogisticRegression(max_iter=200, random_state=42)
log_reg.fit(X_train, y_train)
y_pred_log = log_reg.predict(X_test)
accuracy_log = accuracy_score(y_test, y_pred_log)
print(f"Accuracy (Logistic Regression): {accuracy_log:.2f}")

# Матрица путаницы и отчёт классификации для логистической регрессии
conf_matrix = confusion_matrix(y_test, y_pred_log)
print("Confusion Matrix (Logistic Regression):")
print(conf_matrix)
print("Classification Report (Logistic Regression):")
print(classification_report(y_test, y_pred_log))

# 2. K-Nearest Neighbors (KNN)
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train, y_train)
y_pred_knn = knn.predict(X_test)
accuracy_knn = accuracy_score(y_test, y_pred_knn)
print(f"Accuracy (KNN): {accuracy_knn:.2f}")

# 3. Случайный лес
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)
y_pred_rf = rf.predict(X_test)
accuracy_rf = accuracy_score(y_test, y_pred_rf)
print(f"Accuracy (Random Forest): {accuracy_rf:.2f}")

# 4. Метод опорных векторов (SVM)
svm = SVC(kernel='linear', random_state=42)
svm.fit(X_train, y_train)
y_pred_svm = svm.predict(X_test)
accuracy_svm = accuracy_score(y_test, y_pred_svm)
print(f"Accuracy (SVM): {accuracy_svm:.2f}")

# 5. Метод главных компонент (PCA)
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X)
pca_df = pd.DataFrame(X_pca, columns=['PC1', 'PC2'])
pca_df['target'] = y
print("Explained Variance Ratios (PCA):", pca.explained_variance_ratio_)

# 6. Проверка гипотез (ошибки первого и второго рода)
# Пример: сравнение двух классов (метки 0 и 1)
class_0 = X_train[y_train == 0].mean(axis=0)
class_1 = X_train[y_train == 1].mean(axis=0)
t_stat, p_value = ttest_ind(X_train[y_train == 0], X_train[y_train == 1], axis=0)
alpha = 0.05
reject_null = p_value < alpha

print("Hypothesis Testing Results:")
for feature, p, reject in zip(X.columns, p_value, reject_null):
    print(f"Feature: {feature}, p-value: {p:.3f}, Reject Null: {reject}")

# Добавление шума в числовые признаки
noise_factor = 0.05
X_noisy = X + np.random.normal(0, noise_factor, X.shape)

# Проверка на устойчивость моделей к шуму
log_reg.fit(X_noisy, y_train)
y_pred_noisy = log_reg.predict(X_test)
accuracy_noisy = accuracy_score(y_test, y_pred_noisy)
print(f"Accuracy with Noise (Logistic Regression): {accuracy_noisy:.2f}")

# Изменение 10% меток
y_noisy = y_train.copy()
flip_indices = np.random.choice(y_train.index, size=int(0.1 * len(y_train)), replace=False)
y_noisy[flip_indices] = 1 - y_noisy[flip_indices]  # Инвертируем метки

# Обучение модели на изменённых метках
log_reg.fit(X_train, y_noisy)
y_pred_flipped = log_reg.predict(X_test)
accuracy_flipped = accuracy_score(y_test, y_pred_flipped)
print(f"Accuracy with Flipped Labels (Logistic Regression): {accuracy_flipped:.2f}")


