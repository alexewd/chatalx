import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import mean_squared_error, r2_score, confusion_matrix, classification_report
from scipy.stats import ttest_ind
import matplotlib.pyplot as plt

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

# Визуализация разделения классов
plt.figure(figsize=(10, 6))
plt.scatter(data.loc[data['Gender'] == 0, 'Height'], data.loc[data['Gender'] == 0, 'Weight'], color='blue', alpha=0.5, label='Male')
plt.scatter(data.loc[data['Gender'] == 1, 'Height'], data.loc[data['Gender'] == 1, 'Weight'], color='red', alpha=0.5, label='Female')
plt.title('Gender Classification')
plt.xlabel('Height')
plt.ylabel('Weight')
plt.legend()
plt.show()
