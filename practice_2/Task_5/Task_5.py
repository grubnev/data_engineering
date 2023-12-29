import json
import pandas as pd
import numpy as np
import msgpack
import pickle

# Чтение JSON-файла
with open('rows.json') as json_file:
    data = json.load(json_file)

# Создание DataFrame из JSON-данных
df = pd.DataFrame(data)

# Функция для рассчета характеристик числовых данных
def calculate_numeric_stats(column):
    return {
        'min': column.min(),
        'max': column.max(),
        'mean': column.mean(),
        'sum': column.sum(),
        'std_dev': column.std()
    }

# Функция для рассчета частоты встречаемости текстовых данных
def calculate_text_frequency(column):
    return column.value_counts().to_dict()

# Словарь для сохранения результатов
results = {}

# Итерация по столбцам DataFrame
for column in df.columns:
    if df[column].dtype == 'object':
        results[column] = calculate_text_frequency(df[column])
    elif np.issubdtype(df[column].dtype, np.number):
        results[column] = calculate_numeric_stats(df[column])

# Сохранение результатов в JSON
with open('results.json', 'w') as json_result_file:
    json.dump(results, json_result_file)

# Сохранение DataFrame в различных форматах
df.to_csv('data.csv', index=False)
df.to_json('data.json', orient='records')
df.to_msgpack('data.msgpack')
df.to_pickle('data.pkl')