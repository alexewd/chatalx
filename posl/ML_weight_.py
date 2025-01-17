import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

# Загрузка данных
file_path = 'e:/posl/data/weight-height.csv'
data = pd.read_csv(file_path, delimiter=',')
data['Gender'] = data['Gender'].map({'Male': 0, 'Female': 1})

# Определение признаков (X) и целевой переменной (y)
X = data[['Gender', 'Height']]
y = data['Weight']

# Разделение данных на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Словарь для хранения моделей и их метрик
models = {
    'Linear Regression': LinearRegression(),
    'KNN Regressor': KNeighborsRegressor(n_neighbors=5),
    'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42),
    'SVM (RBF Kernel)': SVR(kernel='rbf')
}

metrics = []

# Обучение моделей и расчет метрик
for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    metrics.append({'Model': name, 'MSE': mse, 'R2': r2})

# Создание таблицы метрик
metrics_df = pd.DataFrame(metrics)
print(metrics_df)

# Визуализация результатов линейной регрессии
plt.figure(figsize=(12, 6))
plt.scatter(X_test['Height'], y_test, color='blue', label='Actual Data', alpha=0.6)
plt.scatter(X_test['Height'], models['Linear Regression'].predict(X_test), color='red', label='Linear Regression Predictions', alpha=0.6)
plt.title('Linear Regression Fit')
plt.xlabel('Height')
plt.ylabel('Weight')
plt.legend()
plt.show()

# Визуализация предсказаний других моделей
plt.figure(figsize=(12, 8))
height_range = np.linspace(X_test['Height'].min(), X_test['Height'].max(), 500)
for name, model in models.items():
    predictions = model.predict(pd.DataFrame({'Gender': np.zeros_like(height_range), 'Height': height_range}))
    plt.plot(height_range, predictions, label=name)

plt.scatter(X_test['Height'], y_test, color='blue', label='Actual Data', alpha=0.6)
plt.title('Model Predictions')
plt.xlabel('Height')
plt.ylabel('Weight')
plt.legend()
plt.show()
