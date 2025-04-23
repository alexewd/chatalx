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

# Вероятность того, что мужчина проживет больше 70 лет: 34.46%  при 66 средней
# Вероятность того, что мужчина проживет больше 75 лет: 18.41%

# Предположим, что 80% мужчин доживают до 60 лет
probability_survive_to_60 = 0.80

# Вероятности дожить до 70 и 75 лет (например, из предыдущих расчетов)
probability_above_70 = 0.60  # Вероятность дожить до 70 лет
probability_above_75 = 0.40  # Вероятность дожить до 75 лет

# Условные вероятности
conditional_probability_above_70 = probability_above_70 / probability_survive_to_60
conditional_probability_above_75 = probability_above_75 / probability_survive_to_60

print(f"Условная вероятность того, что мужчина, доживший до 60 лет, проживет больше 70 лет: {conditional_probability_above_70:.2%}")
print(f"Условная вероятность того, что мужчина, доживший до 60 лет, проживет больше 75 лет: {conditional_probability_above_75:.2%}")

# Данные
average_life_expectancy = 66  # Средняя продолжительность жизни
percent_dying_before_65 = 0.52  # Процент мужчин, не доживающих до 65 лет
percent_surviving_to_65 = 1 - percent_dying_before_65  # Процент мужчин, доживающих до 65 лет

# Предположения для вероятностей доживания до 70 и 75 лет
# Эти значения можно изменить в зависимости от ваших предположений
probability_surviving_to_70 = 0.70  # Предположим, что 70% мужчин, достигших 60 лет, доживают до 70
probability_surviving_to_75 = 0.50  # Предположим, что 50% мужчин, достигших 60 лет, доживают до 75

# Функция для расчета вероятностей
def calculate_survival_probabilities():
    # Вероятность доживания до 70 лет для мужчин, достигших 60 лет
    p_70_given_60 = probability_surviving_to_70
    # Вероятность доживания до 75 лет для мужчин, достигших 60 лет
    p_75_given_60 = probability_surviving_to_75
    
    return p_70_given_60, p_75_given_60

# Получение вероятностей
prob_70, prob_75 = calculate_survival_probabilities()

# Вывод результатов
print(f"Вероятность доживания до 70 лет для мужчин, достигших 60 лет: {prob_70 * 100:.2f}%")
print(f"Вероятность доживания до 75 лет для мужчин, достигших 60 лет: {prob_75 * 100:.2f}%")