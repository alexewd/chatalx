import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import mean_squared_error, r2_score, confusion_matrix, classification_report, roc_curve, auc
from scipy.stats import ttest_ind
import matplotlib.pyplot as plt
import seaborn as sns

# Загрузка данных
file_path = 'e:/posl/data/weight-height.csv'
data = pd.read_csv(file_path)
data['Gender'] = data['Gender'].map({'Male': 0, 'Female': 1})

# Определение признаков (X) и целевой переменной (y)
X = data[['Height', 'Weight']]
y = data['Gender']

# Разделение данных на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Модель классификации: Логистическая регрессия
log_reg = LogisticRegression(max_iter=200, random_state=42)
log_reg.fit(X_train, y_train)
y_pred = log_reg.predict(X_test)
y_pred_prob = log_reg.predict_proba(X_test)[:, 1]

# Матрица путанности
conf_matrix = confusion_matrix(y_test, y_pred)
print("Confusion Matrix:")
print(conf_matrix)

# Отчет классификации
class_report = classification_report(y_test, y_pred, target_names=['Male', 'Female'])
print("Classification Report:")
print(class_report)

# Расчет ошибок первого и второго рода
fp = conf_matrix[0, 1]  # False Positive
fn = conf_matrix[1, 0]  # False Negative
tp = conf_matrix[1, 1]  # True Positive
tn = conf_matrix[0, 0]  # True Negative

error_type_1 = fp / (fp + tn)  # Ошибка первого рода
error_type_2 = fn / (fn + tp)  # Ошибка второго рода

print(f"Error Type I (False Positive Rate): {error_type_1:.2f}")
print(f"Error Type II (False Negative Rate): {error_type_2:.2f}")

# Проверка гипотез (p-value)
class_0 = X_train[y_train == 0]
class_1 = X_train[y_train == 1]
t_stat, p_value = ttest_ind(class_0, class_1, axis=0)
alpha = 0.05
reject_null = p_value < alpha

print("Hypothesis Testing Results:")
for feature, p, reject in zip(X.columns, p_value, reject_null):
    print(f"Feature: {feature}, p-value: {p:.3f}, Reject Null: {reject}")

# Визуализация остатков
residuals = y_test - y_pred
plt.figure(figsize=(10, 6))
sns.histplot(residuals, kde=True, color='purple', bins=30)
plt.title('Residuals Distribution')
plt.xlabel('Residuals')
plt.ylabel('Frequency')
plt.show()

# ROC-кривая и AUC
fpr, tpr, thresholds = roc_curve(y_test, y_pred_prob)
roc_auc = auc(fpr, tpr)

plt.figure(figsize=(10, 6))
plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (area = {roc_auc:.2f})')
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic (ROC)')
plt.legend(loc='lower right')
plt.show()

# Визуализация ошибок классификации
plt.figure(figsize=(10, 6))
plt.scatter(X_test['Height'][y_test != y_pred], X_test['Weight'][y_test != y_pred], color='red', alpha=0.6, label='Misclassified')
plt.scatter(X_test['Height'][y_test == y_pred], X_test['Weight'][y_test == y_pred], color='blue', alpha=0.4, label='Correctly Classified')
plt.title('Classification Errors')
plt.xlabel('Height')
plt.ylabel('Weight')
plt.legend()
plt.show()

##########################
# Отчет по классификации:
# Точность (Precision): Это доля правильных положительных предсказаний.
# Мужчины: 0.92
# Женщины: 0.93
# Полнота (Recall): Это доля правильно классифицированных истинных положительных объектов.
# Мужчины: 0.93
# Женщины: 0.91
# F1-оценка: Гармоническое среднее точности и полноты. Балансирует эти две метрики.
# Мужчины: 0.92
# Женщины: 0.92
# Точность (Accuracy): Общее количество правильных предсказаний.
# 0.92 или 92% всех предсказаний были правильными.
# Макро-усреднение (Macro Average): Среднее значение точности, полноты и F1-оценки по всем классам (Мужчины, Женщины), без учета дисбаланса классов.
# Взвешенное усреднение (Weighted Average): Среднее значение точности, полноты и F1-оценки, взвешенное по количеству истинных примеров каждого класса.
# Ошибки:
# Ошибка типа I (Доля ложноположительных): 0.07 — Это означает, что 7% женщин были ошибочно классифицированы как мужчины.
# Ошибка типа II (Доля ложноотрицательных): 0.09 — Это означает, что 9% мужчин были ошибочно классифицированы как женщины.
# Результаты гипотезного тестирования:
# Рост: p-значение = 0.000, что указывает на то, что рост статистически значим для предсказания пола. Нулевая гипотеза отклоняется.
# Вес: p-значение = 0.000, что также означает, что вес статистически значим для предсказания пола, и нулевая гипотеза отклоняется.
# Вывод:
# Модель демонстрирует хорошие результаты с точностью 92%, и как рост, так и вес являются статистически значимыми признаками для предсказания пола.

# №№№№№№№№№№№№№№№№
# Да, вы правильно понимаете! Этот код можно адаптировать и для других табличных данных с большим количеством признаков, но есть несколько важных моментов, на которые стоит обратить внимание:

# 1. Типы признаков:
# Если ваши данные содержат как числовые, так и категориальные признаки, вам нужно будет их предварительно обработать:
# Для числовых признаков можно использовать их напрямую.
# Для категориальных признаков нужно будет применить методы кодирования, такие как One-Hot Encoding или Label Encoding.
# 2. Масштабирование данных:
# Для некоторых моделей, например, логистической регрессии или методов, чувствительных к масштабированию (например, SVM, KNN), важно нормализовать или стандартизировать числовые признаки. Это делается с помощью StandardScaler или MinMaxScaler из библиотеки sklearn.
# 3. Обработка пропусков:
# Если в ваших данных есть пропуски, их нужно будет корректно обработать, например, с помощью методов SimpleImputer или KNNImputer.
# 4. Выбор модели:
# В зависимости от задачи и типа данных (классификация, регрессия, или другие задачи), вам нужно будет выбрать подходящую модель. Например:
# Для классификации вы можете использовать модели, такие как логистическая регрессия, случайный лес, XGBoost, нейронные сети и другие.
# Для регрессии подойдут такие модели, как линейная регрессия, случайный лес для регрессии, XGBoost для регрессии и так далее.
# 5. Параметры гипотезных тестов:
# Если вы добавляете больше признаков, вы должны провести тесты значимости для каждого нового признака (например, через p-значения), чтобы понять, какие из них действительно влияют на целевую переменную.
# 6. Параметры модели и кросс-валидация:
# Когда количество признаков увеличивается, возможно, потребуется использовать кросс-валидацию для оценки производительности модели, чтобы избежать переобучения, а также провести настройку гиперпараметров с помощью методов, таких как GridSearchCV или RandomizedSearchCV.
# 7. Оценка результатов:
# В зависимости от задач (классификация или регрессия) можно будет использовать различные метрики (например, для классификации — точность, F1-оценка, для регрессии — MAE, RMSE и т.д.).
# Итак, если ваши данные будут немного отличаться по структуре, вам нужно будет адаптировать эти шаги, но общий подход останется тем же — разделение на обучающую и тестовую выборки, обучение модели, оценка ее результатов и проверка статистической значимости признаков.







# Is this conversation helpful so far?













