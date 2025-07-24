import pandas as pd
import json
import os

# Загрузка данных из JSON
data_dir = 'database'
file_path = os.path.abspath(os.path.join(data_dir, 'dataset_career_test.json'))

if not os.path.exists(file_path):
    print(f"Ошибка: Файл {file_path} не найден!")
    exit(1)

with open(file_path, 'r', encoding='utf-8') as f:
    dataset = json.load(f)

# Преобразование в DataFrame
df = pd.DataFrame(dataset)

# Функция для валидации датасета
def validate_dataset(df):
    issues = []
    
    # Проверка обязательных полей
    required_fields = ['class', 'region', 'avg_grade', 'favorite_subjects', 'hard_subjects', 'subject_scores']
    for field in required_fields:
        if df[field].isnull().any():
            issues.append(f"Пропуски в {field}")

    # Проверка размеров списков
    if not all(df['favorite_subjects'].apply(len) == 3):
        issues.append("Неверное количество любимых предметов (должно быть 3)")
    if not all(df['hard_subjects'].apply(len) == 2):
        issues.append("Неверное количество сложных предметов (должно быть 2)")
    if not all(df['interests'].apply(lambda x: 1 <= len(x) <= 5)):
        issues.append("Количество интересов должно быть от 1 до 5")
    if not all(df['values'].apply(lambda x: 1 <= len(x) <= 3)):
        issues.append("Количество ценностей должно быть от 1 до 3")

    # Проверка пересечений favorite_subjects и hard_subjects
    for index, row in df.iterrows():
        if any(subject in row['hard_subjects'] for subject in row['favorite_subjects']):
            issues.append(f"Пересечение между favorite_subjects и hard_subjects в записи {index}")

    # Проверка оценок subject_scores (1-5)
    valid_subjects = ["Математика", "Русский язык", "Химия", "Биология", "Физика", "Информатика", "История", "География", "Литература", "Английский язык", "Обществознание"]
    for index, row in df.iterrows():
        scores = row['subject_scores']
        for subject, score in scores.items():
            if subject not in valid_subjects or not (1 <= score <= 5):
                issues.append(f"Неверная оценка {score} для предмета {subject} в записи {index}")
        
        # Проверка диапазонов оценок по favorite_subjects (4-5) и hard_subjects (1-2)
        for subject in row['favorite_subjects']:
            if scores.get(subject, 0) not in [4, 5]:
                issues.append(f"Оценка по любимому предмету {subject} ({scores.get(subject)}) должна быть 4 или 5 в записи {index}")
        for subject in row['hard_subjects']:
            if scores.get(subject, 0) not in [1, 2]:
                issues.append(f"Оценка по сложному предмету {subject} ({scores.get(subject)}) должна быть 1 или 2 в записи {index}")
        
        # Проверка MBTI-оценок (1-7)
        mbti_scores = row['mbti_scores']
        for q in [f'q{i}' for i in range(11, 36)]:
            if mbti_scores.get(q, 0) not in range(1, 8):
                issues.append(f"Неверная MBTI-оценка для {q} ({mbti_scores.get(q)}) в записи {index}, должна быть 1-7")

    return issues

# Выполнение валидации
validation_issues = validate_dataset(df)

# Вывод результатов
if not validation_issues:
    print("Датасет валиден!")
else:
    print("Найдены следующие проблемы в датасете:")
    for issue in validation_issues:
        print(f"- {issue}")

# Сохранение отчёта о валидации (опционально)
with open(os.path.join(data_dir, 'validation_report.txt'), 'w', encoding='utf-8') as f:
    f.write("Отчёт о валидации датасета:\n")
    if not validation_issues:
        f.write("Датасет валиден!\n")
    else:
        f.write("Найдены следующие проблемы:\n")
        for issue in validation_issues:
            f.write(f"- {issue}\n")
print(f"Отчёт о валидации сохранён в {os.path.join(data_dir, 'validation_report_dataset_career_test.txt')}")
