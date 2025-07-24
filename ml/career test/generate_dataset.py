import random
import json
import os

# Списки для генерации
classes = ["9", "10", "11"]
regions = ["Москва/Московская обл.", "Санкт-Петербург/Ленинградская обл.", "Центральная Россия", "Урал", "Сибирь", "Дальний Восток", "Южная Россия", "Северо-Запад"]
grade_ranges = ["3.0-3.5", "3.6-4.0", "4.1-4.5", "4.6-5.0"]
subjects = ["Математика", "Информатика", "Химия", "Биология", "Физика", "Литература", "История", "География", "Русский язык", "Английский язык", "Обществознание"]
interests = ["Помогать людям", "Разрабатывать технологии", "Делать эксперименты", "Общаться и вести переговоры", "Работать с цифрами", "Организовывать проекты", "Писать и читать", "Делать что-то руками", "Художественное творчество", "Путешествия"]
values = ["Высокий доход", "Стабильность", "Помощь другим", "Самореализация", "Свобода", "Карьерный рост", "Работа в команде", "Удалённая работа"]
roles = ["Руководителем", "Исследователем и стратегом", "Исполнителем", "Вдохновителем и коммуникатором"]
places = ["В лаборатории", "В переговорной комнате", "На стройке", "За компьютером"]
styles = ["По чёткому алгоритму", "Спонтанно"]
excludes = ["Постоянно общаться", "Работать руками", "Читать и писать", "Работать без творчества", "Брать ответственность"]

# Функция для генерации subject_scores, согласованных с avg_grade и предпочтениями
def generate_subject_scores(avg_grade_range, favorite_subjects, hard_subjects):
    if avg_grade_range == "3.0-3.5":
        base_min, base_max = 2.0, 3.5
    elif avg_grade_range == "3.6-4.0":
        base_min, base_max = 3.0, 4.0
    elif avg_grade_range == "4.1-4.5":
        base_min, base_max = 3.5, 4.5
    else:  # "4.6-5.0"
        base_min, base_max = 4.0, 5.0
    
    scores = {}
    # Оценки для favorite_subjects (4-5, самые высокие)
    for subject in favorite_subjects:
        score = random.randint(4, 5)
        scores[subject] = score
    
    # Оценки для hard_subjects (1-2, самые низкие)
    for subject in hard_subjects:
        score = random.randint(1, 2)
        scores[subject] = score
    
    # Оценки для остальных предметов (средние, в диапазоне base_min-base_max)
    other_subjects = [s for s in subjects if s not in favorite_subjects and s not in hard_subjects]
    for subject in other_subjects:
        score = max(1, min(5, round(random.uniform(base_min, base_max), 1)))
        scores[subject] = int(score)
    
    # Корректировка среднего, чтобы соответствовать avg_grade
    all_scores = list(scores.values())
    target_avg = (float(avg_grade_range.split('-')[0]) + float(avg_grade_range.split('-')[1])) / 2
    current_avg = sum(all_scores) / len(all_scores)
    if abs(current_avg - target_avg) > 0.5:
        # Корректируем одну из оценок среди остальных предметов
        idx = random.choice([i for i, s in enumerate(scores.keys()) if s in other_subjects])
        adjustment = target_avg - current_avg
        all_scores[idx] = max(1, min(5, round(all_scores[idx] + adjustment, 0)))
        scores[list(scores.keys())[idx]] = all_scores[idx]
    
    return scores

# Генерация 1000 записей
dataset = []
for _ in range(1000):
    avg_grade = random.choice(grade_ranges)
    # Выбор favorite_subjects и hard_subjects без пересечений
    all_subjects = subjects.copy()
    favorite_subjects = random.sample(all_subjects, 3)
    all_subjects = [s for s in all_subjects if s not in favorite_subjects]
    hard_subjects = random.sample(all_subjects, 2)
    
    record = {
        "class": random.choice(classes),
        "region": random.choice(regions),
        "avg_grade": avg_grade,
        "favorite_subjects": favorite_subjects,
        "hard_subjects": hard_subjects,
        "subject_scores": generate_subject_scores(avg_grade, favorite_subjects, hard_subjects),
        "interests": random.sample(interests, random.randint(1, 5)),
        "values": random.sample(values, random.randint(1, 3)),
        "mbti_scores": {f"q{i}": random.randint(1, 7) for i in range(11, 36)},
        "work_preferences": {
            "role": random.choice(roles),
            "place": random.choice(places),
            "style": random.choice(styles),
            "exclude": random.sample(excludes, random.randint(1, 3))
        }
    }
    dataset.append(record)
    print(f"Сгенерирована запись {_ + 1}")  # Отладочный вывод для каждой записи

# Проверка, что данные сгенерированы
if not dataset:
    print("Ошибка: Датасет пустой, данные не сгенерированы!")
else:
    print(f"Успешно сгенерировано {len(dataset)} записей")

# Создание папки data, если она отсутствует
data_dir = 'database'
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

# Определение абсолютного пути для файла
file_path = os.path.abspath(os.path.join(data_dir, 'dataset_career_test.json'))

try:
    # Сохранение датасета
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)
    print(f"Синтетический датасет успешно сохранён в {file_path}")

    # Проверка, что файл не пустой
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        if content:
            print(f"Файл содержит данные, размер: {len(content)} байт")
        else:
            print("Ошибка: Файл пустой после сохранения!")
except IOError as e:
    print(f"Ошибка при сохранении файла: {e}")
except Exception as e:
    print(f"Неожиданная ошибка: {e}")
