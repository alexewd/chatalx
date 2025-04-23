import pandas as pd

# Чтение CSV файла
df = pd.read_csv('c:\\bac_c\\nekropol\\burials_x_i.txt.csv', encoding='utf-8')
import pandas as pd
import numpy as np
from IPython.display import display

# Чтение CSV файла
# df = pd.read_csv('your_file.csv')

# Удаление лишних пробелов в названиях столбцов
df.columns = df.columns.str.strip()

# Замена 'NA' на NaN и удаление пробелов в значениях
df['year_born'] = df['year_born'].replace('NA', np.nan).str.strip()
df['year_death'] = df['year_death'].replace('NA', np.nan).str.strip()

# Удаление строк с NA
df = df.dropna()

# Преобразование столбцов в формат год
df['year_born'] = pd.to_numeric(df['year_born'], errors='coerce')
df['year_death'] = pd.to_numeric(df['year_death'], errors='coerce')

# Удаление строк с NaN после преобразования
df = df.dropna()

# Создание нового столбца 'live' с вычислением разности
df['live'] = df['year_death'] - df['year_born']

# Преобразование столбцов в целые числа
df['year_born'] = df['year_born'].astype(int)
df['year_death'] = df['year_death'].astype(int)
df['live'] = df['live'].astype(int)

# Вывод результата
print(df)

# Вывод результата в табличном виде
display(df[['name', 'year_born', 'year_death', 'live']])

# Сохранение результата в новый CSV файл
df[['name', 'year_born', 'year_death', 'live']].to_csv('output_file_x_i.csv', index=False, encoding='utf-8-sig')

# Вывод среднего значения по столбцу 'live'
average_live = df['live'].mean()
print(f"Средняя продолжительность жизни: {average_live:.2f} лет")

# Вывод среднего значения по столбцу 'live'
average_live = df['live'].mean()
print(f"Средняя продолжительность жизни: {average_live:.2f} лет")

# Предположим, что у нас есть следующие данные для анализа
average_life_europe_men = 70  # Средняя продолжительность жизни мужчин в Европе
average_life_europe_women = 75  # Средняя продолжительность жизни женщин в Европе
average_life_usa_men = 73  # Средняя продолжительность жизни мужчин в США
average_life_usa_women = 78  # Средняя продолжительность жизни женщин в США

# Вычисление разницы
difference_europe_men = average_live - average_life_europe_men
difference_europe_women = average_live - average_life_europe_women
difference_usa_men = average_live - average_life_usa_men
difference_usa_women = average_live - average_life_usa_women

print(f"Разница с средней продолжительностью жизни мужчин в Европе: {difference_europe_men:.2f} лет")
print(f"Разница с средней продолжительностью жизни женщин в Европе: {difference_europe_women:.2f} лет")
print(f"Разница с средней продолжительностью жизни мужчин в США: {difference_usa_men:.2f} лет")
print(f"Разница с средней продолжительностью жизни женщин в США: {difference_usa_women:.2f} лет")

# Вычисление средней продолжительности жизни, исключая значения меньше 18 лет
average_live_excluding_young = df[df['live'] >= 18]['live'].mean()
print(f"Средняя продолжительность жизни (исключая детей и подростков): {average_live_excluding_young:.2f} лет")

# Вычисление средней продолжительности жизни среди тех, кто прожил больше 40 лет
average_live_above_40 = df[df['live'] > 40]['live'].mean()
print(f"Средняя продолжительность жизни среди тех, кто прожил больше 40 лет: {average_live_above_40:.2f} лет")

# Вычисление медианы по столбцу 'live'
median_live = df['live'].median()
print(f"Медиана продолжительности жизни: {median_live:.2f} лет")

import numpy as np
import scipy.stats as stats

# Средняя продолжительность жизни
mean_life_expectancy = 66
# Стандартное отклонение (примерное значение)
std_dev = 10

# Вычисление вероятностей
probability_above_70 = 1 - stats.norm.cdf(70, loc=mean_life_expectancy, scale=std_dev)
probability_above_75 = 1 - stats.norm.cdf(75, loc=mean_life_expectancy, scale=std_dev)

print(f"Вероятность того, что мужчина проживет больше 70 лет: {probability_above_70:.2%}")
print(f"Вероятность того, что мужчина проживет больше 75 лет: {probability_above_75:.2%}")

