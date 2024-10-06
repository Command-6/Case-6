import pandas as pd
import spacy
from spacy.util import minibatch
from sklearn.model_selection import train_test_split
from spacy.training.example import Example
from spacy.util import minibatch

df = pd.read_csv('dataset.csv',quotechar='"', on_bad_lines='skip', encoding="utf-8")

# Вывод названий всех колонок
print(df.columns)
# Загрузка датасета из CSV файла
df = pd.read_csv('dataset.csv',on_bad_lines='skip', encoding="utf-8")

# Оставляем только те строки, где есть разметка (без пустых значений в колонке 'sentiment')


# Преобразуем данные в подходящий формат: положительные метки в 1, отрицательные в 0
df['sentiment'] = df['sentiment'].apply(lambda x: 1 if x == 'Positive' else 0)

# Оставляем только необходимые колонки для обучения: текст и метка
df = df[['text', 'sentiment']]

train_data, test_data = train_test_split(df, test_size=0.2, random_state=42)
def convert_to_spacy_format(data):
    return [(row['text'], {"cats": {"POSITIVE": row['sentiment'] == 1, "NEGATIVE": row['sentiment'] == 0}}) for _, row in data.iterrows()]

train_data = convert_to_spacy_format(train_data)
test_data = convert_to_spacy_format(test_data)

nlp = spacy.blank("ru")
# Добавляем pipeline для текстовой классификации, если его еще нет
if "textcat" not in nlp.pipe_names:
    textcat = nlp.add_pipe("textcat", last=True)
    
# Определяем метки для классификации: позитив и негатив
textcat.add_label("POSITIVE")
textcat.add_label("NEGATIVE")

# Количество эпох обучения
n_iter = 10

# Начинаем обучение и получаем оптимизатор
optimizer = nlp.begin_training()

# Цикл обучения
for i in range(n_iter):
    losses = {}

    # Разбиваем данные на мини-батчи
    batches = minibatch(train_data, size=8)

    for batch in batches:
        examples = []
        for text, annotations in batch:
            # Создаем пример для обучения
            doc = nlp.make_doc(text)
            example = Example.from_dict(doc, annotations)
            examples.append(example)
        
        # Обновляем модель
        nlp.update(examples, sgd=optimizer, losses=losses)

    print(f"Losses at iteration {i}: {losses}")

correct = 0
total = 0

for text, annotations in test_data:
    doc = nlp(text)
    predicted_label = doc.cats['POSITIVE'] >= 0.5  # Если вероятность >= 0.5, то это позитив
    true_label = annotations['cats']['POSITIVE'] == 1  # Истинная метка
    if predicted_label == true_label:
        correct += 1
    total += 1

accuracy = correct / total
print(f"Точность модели: {accuracy}")

# Сохраняем модель в директорию
nlp.to_disk("ru_sentiment_model")

print("Модель успешно сохранена!")

