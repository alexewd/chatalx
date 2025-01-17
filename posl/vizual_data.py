import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.datasets import load_iris

# Загрузка данных (например, Iris dataset)
data = load_iris()
X = data.data
y = data.target

# Применяем PCA для редукции размерности
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X)

# Визуализируем данные в 2D
plt.figure(figsize=(8, 6))
plt.scatter(X_pca[:, 0], X_pca[:, 1], c=y, cmap='viridis', edgecolor='k', s=100)
plt.colorbar(label='Класс')
plt.xlabel('Первая главная компонента')
plt.ylabel('Вторая главная компонента')
plt.title('PCA - Визуализация данных')
plt.show()


import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
from sklearn.datasets import load_iris

# Загрузка данных (например, Iris dataset)
data = load_iris()
X = data.data
y = data.target

# Применяем t-SNE для редукции размерности
tsne = TSNE(n_components=2, random_state=42)
X_tsne = tsne.fit_transform(X)

# Визуализируем данные в 2D
plt.figure(figsize=(8, 6))
plt.scatter(X_tsne[:, 0], X_tsne[:, 1], c=y, cmap='viridis', edgecolor='k', s=100)
plt.colorbar(label='Класс')
plt.xlabel('t-SNE компонента 1')
plt.ylabel('t-SNE компонента 2')
plt.title('t-SNE - Визуализация данных')
plt.show()

