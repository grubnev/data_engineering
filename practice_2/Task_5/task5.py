import pandas as pd
import numpy as np
import json
import msgpack

df = pd.read_csv('NYPD_Arrest_Data__Year_to_Date_.csv')

selected_fields = ['ARREST_KEY', 'ARREST_DATE', 'PD_CD', 'PD_DESC', 'KY_CD', 'OFNS_DESC', 'AGE_GROUP', 'PERP_SEX', 'PERP_RACE']
selected_df = df[selected_fields]

# Рассчитываем характеристики для числовых полей
numeric_fields = ['ARREST_KEY', 'PD_CD', 'KY_CD']
numeric_stats = selected_df[numeric_fields].describe().to_dict()

# Рассчитываем частоту встречаемости для текстовых полей
text_fields = ['ARREST_DATE', 'PD_DESC', 'OFNS_DESC', 'AGE_GROUP', 'PERP_SEX', 'PERP_RACE']
text_freq = {field: selected_df[field].value_counts().to_dict() for field in text_fields}

# Сохраняем результаты в JSON файл
result_json = {
    'numeric_stats': numeric_stats,
    'text_freq': text_freq
}

with open('result_stats.json', 'w') as json_file:
    json.dump(result_json, json_file)

# Сохраняем набор данных в разных форматах
df.to_csv('data.csv', index=False)
df.to_json('data.json', orient='records')
df.to_pickle('data.pkl')
with open('data.msgpack', 'wb') as msgpack_file:
    packed_data = msgpack.packb(df.to_dict(orient='records'))
    msgpack_file.write(packed_data)
