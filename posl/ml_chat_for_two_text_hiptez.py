import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.decomposition import PCA
from sklearn.metrics import accuracy_score, mean_squared_error, confusion_matrix, classification_report
from sklearn.utils import resample
from scipy.stats import ttest_ind

# Загрузка набора данных Iris
data = load_iris()
X = pd.DataFrame(data.data, columns=data.feature_names)
y = pd.Series(data.target, name='target')

# Разделение данных на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

# 1. Линейная регрессия (используем одну метрику как пример)
lin_reg = LinearRegression()
lin_reg.fit(X_train, y_train)
y_pred_reg = lin_reg.predict(X_test)
mse = mean_squared_error(y_test, y_pred_reg)
print(f"Mean Squared Error (Linear Regression): {mse:.2f}")

# 2. Логистическая регрессия
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

# 3. K-Nearest Neighbors (KNN)
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train, y_train)
y_pred_knn = knn.predict(X_test)
accuracy_knn = accuracy_score(y_test, y_pred_knn)
print(f"Accuracy (KNN): {accuracy_knn:.2f}")

# 4. Перекрёстная проверка (на примере логистической регрессии)
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
cross_val_scores = cross_val_score(log_reg, X, y, cv=skf, scoring='accuracy')
print(f"Cross-Validation Accuracy (Logistic Regression): {cross_val_scores.mean():.2f} (+/- {cross_val_scores.std():.2f})")

# 5. Бутстреп-оценивание
n_iterations = 100
bootstrap_scores = []
for _ in range(n_iterations):
    X_resampled, y_resampled = resample(X_train, y_train, random_state=42)
    log_reg.fit(X_resampled, y_resampled)
    bootstrap_scores.append(log_reg.score(X_test, y_test))
print(f"Bootstrap Accuracy (Logistic Regression): {np.mean(bootstrap_scores):.2f} (+/- {np.std(bootstrap_scores):.2f})")

# 6. Случайный лес
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)
y_pred_rf = rf.predict(X_test)
accuracy_rf = accuracy_score(y_test, y_pred_rf)
print(f"Accuracy (Random Forest): {accuracy_rf:.2f}")

# 7. Метод опорных векторов (SVM)
svm = SVC(kernel='linear', random_state=42)
svm.fit(X_train, y_train)
y_pred_svm = svm.predict(X_test)
accuracy_svm = accuracy_score(y_test, y_pred_svm)
print(f"Accuracy (SVM): {accuracy_svm:.2f}")

# 8. Метод главных компонент (PCA)
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X)
pca_df = pd.DataFrame(X_pca, columns=['PC1', 'PC2'])
pca_df['target'] = y
print("Explained Variance Ratios (PCA):", pca.explained_variance_ratio_)

# 9. Проверка гипотез (ошибки первого и второго рода)
# Пример: сравнение двух классов (0 и 1)
class_0 = X_train[y_train == 0].mean(axis=0)
class_1 = X_train[y_train == 1].mean(axis=0)
t_stat, p_value = ttest_ind(X_train[y_train == 0], X_train[y_train == 1], axis=0)
alpha = 0.05
reject_null = p_value < alpha

print("Hypothesis Testing Results:")
for feature, p, reject in zip(X.columns, p_value, reject_null):
    print(f"Feature: {feature}, p-value: {p:.3f}, Reject Null: {reject}")
