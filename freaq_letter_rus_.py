import collections
import pandas as pd

# Текст для анализа
text = '''Когда человек сознательно или интуитивно выбирает себе в жизни какую-то цель, жизненную задачу, он невольно дает себе оценку. По тому, ради чего человек живет, можно судить и о его самооценке - низкой или высокой.
Если человек живет, чтобы приносить людям добро, облегчать их страдания, давать людям радость, то он оценивает себя на уровне этой своей человечности. Он ставит себе цель, достойную человека.
Только такая цель позволяет человеку прожить свою жизнь с достоинством и получить настоящую радость. Да, радость! Подумайте: если человек ставит себе задачей увеличивать в жизни добро, приносить людям счастье, какие неудачи могут его постигнуть? Не тому помочь? Но много ли людей не нуждаются в помощи?
Если жить только для себя, своими мелкими заботами о собственном благополучии, то от прожитого не останется и следа. Если же жить для других, то другие сберегут то, чему служил, чему отдавал силы.
Можно по-разному определять цель своего существования, но цель должна быть. Надо иметь и принципы в жизни. Одно правило в жизни должно быть у каждого человека, в его цели жизни, в его принципах жизни, в его поведении: надо прожить жизнь с достоинством, чтобы не стыдно было вспоминать.
Достоинство требует доброты, великодушия, умения не быть эгоистом, быть правдивым, хорошим другом, находить радость в помощи другим.
Ради достоинства жизни надо уметь отказываться от мелких удовольствий и немалых тоже… Уметь извиняться, признавать перед другими ошибку - лучше, чем врать.
Обманывая, человек прежде всего обманывает самого себя, ибо он думает, что успешно соврал, а люди поняли и из деликатности промолчали.
Жизнь - прежде всего творчество, но это не значит, что каждый человек, чтобы жить, должен родиться художником, балериной или ученым. Можно творить просто добрую атмосферу вокруг себя. Человек может принести с собой атмосферу подозрительности, какого-то тягостного молчания, а может внести сразу радость, свет. Вот это и есть творчество.'''

# Приводим текст к нижнему регистру
text = text.lower()

# Считаем частоту букв
frequency = collections.Counter(text)

# Убираем пробелы и символы, не являющиеся буквами
total_letters = sum(frequency[letter] for letter in frequency if letter.isalpha())

# Таблица частот русского языка
russian_frequency = {
    "а": 0.062, "б": 0.014, "в": 0.038, "г": 0.013, "д": 0.025,
    "е": 0.072, "ж": 0.007, "з": 0.016, "и": 0.062, "й": 0.010,
    "к": 0.028, "л": 0.035, "м": 0.026, "н": 0.053, "о": 0.090,
    "п": 0.023, "р": 0.040, "с": 0.045, "т": 0.053, "у": 0.021,
    "ф": 0.002, "х": 0.009, "ц": 0.004, "ч": 0.012, "ш": 0.006,
    "щ": 0.003, "ъ": 0.000, "ы": 0.019, "ь": 0.014, "э": 0.003,
    "ю": 0.006, "я": 0.018
}

# Подготавливаем данные для датафрейма
data = []
for letter, count in frequency.items():
    if letter.isalpha():
        # Рассчитываем относительную частоту в тексте
        relative_frequency = count / total_letters
        relative_frequency_percent = round(relative_frequency * 100, 3)

        # Сравниваем с таблицей частот
        expected_frequency = russian_frequency.get(letter, 0)
        ratio = round(relative_frequency / expected_frequency, 2) if expected_frequency > 0 else None

        # Добавляем данные в список
        data.append({
            "Буква": letter,
            "Частота в тексте (%)": relative_frequency_percent,
            "Ожидаемая частота (%)": round(expected_frequency * 100, 3),
            "Соотношение к ожиданию": ratio
        })

# Создаем датафрейм
df = pd.DataFrame(data)

# Сортируем датафрейм по частоте в тексте
df = df.sort_values(by="Частота в тексте (%)", ascending=False)

# Выводим датафрейм
print(df)
