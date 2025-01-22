import pandas as pd
import dedupe
from dedupe import variables

# Пример данных
data = {
    'id': [1, 2, 3, 4, 5],
    'name': ['John Doe', 'Jane Doe', 'Jon Doe', 'Johnathan Doe', 'Jane Dowe'],
    'address': ['123 Elm St', '123 Elm St', '123 Elm St', '124 Elm St', '125 Elm St']
}

# Преобразуем в DataFrame
df = pd.DataFrame(data)

# Подготовим данные для dedupe
data_dict = df.to_dict(orient='records')

# Указываем поля для dedupe с использованием новых объектов переменных
fields = [
    variables.String('name'),
    variables.String('address')
]

# Создаем объект для dedupe
deduper = dedupe.Dedupe(fields)

# Подготовка данных для обучения
deduper.prepare_training(data_dict)

# Отображение пар для размечания
deduper.display_training(data_dict)

# Проводим обучение
deduper.train()

# Поиск дубликатов
threshold = 0.5
clustered_dupes = deduper.match(data_dict, threshold)

# Выводим результаты
for cluster in clustered_dupes:
    print(f"Cluster {cluster[0]}:")
    for record in cluster[1]:
        print(f"  {df.iloc[record]['name']}, {df.iloc[record]['address']}")
