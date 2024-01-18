import pandas as pd
import numpy as np
import json

#Чтение CSV файла
data = pd.read_csv('NYPD_Arrest_Data__Year_to_Date_.csv')

#Отбор нужных полей
selected_fields = data[['ARREST_KEY', 'ARREST_DATE', 'PD_CD', 'PD_DESC', 'KY_CD', 'OFNS_DESC', 'ARREST_BORO', 'AGE_GROUP', 'PERP_SEX', 'PERP_RACE']]

#Рассчет числовых характеристик
numeric_fields = ['ARREST_KEY', 'PD_CD', 'KY_CD']
numeric_characteristics = {}

for field in numeric_fields:
    field_data = selected_fields[field]
    numeric_characteristics[field] = {
    'min': np.min(field_data),
    'max': np.max(field_data),
    'mean': np.mean(field_data),
    'sum': np.sum(field_data),
    'std': np.std(field_data)
    }

#Рассчет частоты встречаемости текстовых данных
text_fields = ['ARREST_DATE', 'PD_DESC', 'OFNS_DESC', 'ARREST_BORO', 'AGE_GROUP', 'PERP_SEX', 'PERP_RACE']
text_frequencies = {}

for field in text_fields:
    field_data = selected_fields[field]
    value_counts = field_data.value_counts().to_dict()
    text_frequencies[field] = value_counts

#Сохранение результатов числовых характеристик в JSON
with open('numeric_characteristics.json', 'w') as file:
    json.dump(numeric_characteristics, file)

#Сохранение результатов частоты встречаемости текстовых данных в JSON
with open('text_frequencies.json', 'w') as file:
    json.dump(text_frequencies, file)

#Сохранение набора данных в разных форматах
selected_fields.to_csv('selected_fields.csv', index=False)
selected_fields.to_json('selected_fields.json', orient='records')
selected_fields.to_msgpack('selected_fields.msgpack')
selected_fields.to_pickle('selected_fields.pkl')

#Сравнение размеров файлов
csv_size = os.path.getsize('selected_fields.csv')
json_size = os.path.getsize('selected_fields.json')
msgpack_size = os.path.getsize('selected_fields.msgpack')
pkl_size = os.path.getsize('selected_fields.pkl')

print("Size of selected_fields.csv: ", csv_size)
print("Size of selected_fields.json: ", json_size)
print("Size of selected_fields.msgpack: ", msgpack_size)
print("Size of selected_fields.pkl: ", pkl_size)