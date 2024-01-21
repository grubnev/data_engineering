import pandas as pd
import matplotlib
import numpy as np
import json
import os

def write_to_json(file_name, data):
    with open(file_name, "w", encoding="UTF-8") as f:
        f.write(json.dumps(data))
    print(f"Запись успешно выполнена в {file_name}")

def read_file(file_name):
    return pd.read_csv(file_name)
    #df=pd.read_csv(file_name, chunksize=chunksize, compression='gzip'

def get_memory_stat_by_column(df):
    # сколько памяти занимает каждая колонка
    memory_usage_stat = df.memory_usage(deep=True)
    # сколько всего места занимает файл
    total_memory_usage = memory_usage_stat.sum()
    print(f"file size       ={file_size // 1024:10} кб")
    print(f"file in memory size ={total_memory_usage // 1024:10} кб")
    column_stat = list()
    for key in df.dtypes.keys():
        column_stat.append({
            "column_name": key,
            "memory_abs": memory_usage_stat[key] // 1024,
            "memory_per": round(memory_usage_stat[key] / total_memory_usage * 100, 4),
            "dtype": str(df.dtypes[key])
        })
        # вычислить для каждой колонки занимаемый объем памяти, долю от общего объема, а также выяснить тип данных
    column_stat.sort(key=lambda x: x['memory_abs'], reverse=True)
    for column in column_stat:
        print(f"{column['column_name']:30}: {column['memory_abs']:10} кб: {column['memory_per']:10}%: {column['dtype']}")

def mem_usage(pandas_obj):
    if isinstance(pandas_obj, pd.DataFrame):
        usage_b = pandas_obj.memory_usage(deep=True).sum()
    else: # если не df а серия
        usage_b = pandas_obj.memory_usage(deep=True)
    usage_mb = usage_b/1024**2
    return "{:03.2f} MB".format(usage_mb)

def opt_obj(df):
    converted_obj=pd.DataFrame()
    dataset_obj=df.select_dtypes(include=['object']).copy() # все колонки по типам
    print(dataset_obj.describe())
    # Преобразовать все колонки с типом данных «object» в категориальные,
    # если количество уникальных значений колонки составляет менее 50%.
    for col in dataset_obj.columns:
        num_unique_values=len(dataset_obj[col].unique()) # кол-во уникальных знач
        num_total_values=len(dataset_obj[col]) # всего
        if num_unique_values / num_total_values < 0.5: # если отношение меньше 50%, вводим категориальное поле
            converted_obj.loc[:, col] = dataset_obj[col].astype('category')
        else:
            converted_obj.loc[:, col] = dataset_obj[col]

    print(mem_usage(dataset_obj))
    print(mem_usage((converted_obj)))
    return converted_obj

# Понижающее преобразование
def opt_int(df):
    dataset_int = df.select_dtypes(include=['int'])
    """
    downcast:
            - 'integer' or 'signed': smallest signed int dtype (min.:np.int8)
            - 'unsigned': smallest unsigned int dtype (min.: np.uint8)
            - 'float': smallest float dtype (min.: np.float32)
    """
    converted_int = dataset_int.apply(pd.to_numeric, downcast='unsigned') # оптимизировать формат
    print(mem_usage(dataset_int))
    print(mem_usage(converted_int))
    # как изменились типы
    compare_ints=pd.concat([dataset_int.dtypes, converted_int.dtypes], axis=1)
    compare_ints.columns=['before', 'after']
    compare_ints.apply(pd.Series.value_counts)
    print(compare_ints)
    return converted_int

def opt_float(df):
    dataset_float = df.select_dtypes(include=['float'])
    converted_float = dataset_float.apply(pd.to_numeric, downcast='float')

    print(mem_usage(dataset_float))
    print(mem_usage(converted_float))

    compare_floats = pd.concat([dataset_float.dtypes, converted_float.dtypes], axis=1)
    compare_floats.columns=['before', 'after']
    compare_floats.apply(pd.Series.value_counts)
    print(compare_floats)
    return converted_float

###-------------------------------------------------------------------------------------###

# # 1 датасет
# file_name="data/[1]game_logs.csv"
# column_names = ['date', 'number_of_game', 'day_of_week', 'park_id', 'v_manager_name', 'length_minutes', 'v_hits', 'h_hits', 'h_walks', 'h_errors']

# #2 датасет
# file_name="data/CIS_Automotive_Kaggle_Sample.csv"
# column_names = ['brandName', 'vf_ModelYear', 'isNew', 'askPrice', 'color', 'vf_Model', 'modelName', 'vf_Seats', 'vf_Turbo', 'vf_TrailerType']

# #3 датасет
# file_name="data/[3]flights.csv"
# column_names = ['DEPARTURE_DELAY', 'DEPARTURE_TIME', 'TAXI_OUT', 'AIR_TIME', 'ARRIVAL_TIME', 'ARRIVAL_DELAY', 'DESTINATION_AIRPORT', 'YEAR', 'AIRLINE', 'CANCELLATION_REASON']

# #4 датасет
# file_name="data/[4]vacancies.csv.gz"
# column_names = ["accept_incomplete_resumes", "salary_from", "salary_to", "prof_classes_found", "experience_name", "area_name", "address_lat", "address_lng", "has_test"]

# #5 датасет
# file_name="data/[5]asteroid.zip"
# column_names =  ["full_name", "diameter", "class", "H", "albedo", "epoch_cal", "sigma_e", "sigma_a", "sigma_q", "sigma_i"]

###-------------------------------------------------------------------------------------###


df=read_file(file_name)
file_size=os.path.getsize(file_name)
column_stat = get_memory_stat_by_column(df)

# get_memory_stat_by_column(df)
# dataset.info(memory_usage='deep')
# print(dataset.shape)

optimized_dataset=df.copy()

converted_obj=opt_obj(df)
converted_int=opt_int(df)
converted_float=opt_float(df)

optimized_dataset[converted_obj.columns]=converted_obj
optimized_dataset[converted_int.columns]=converted_int
optimized_dataset[converted_float.columns]=converted_float

print(mem_usage(df))
print(mem_usage(optimized_dataset))
optimized_dataset.info(memory_usage='deep')

# Повторный анализ файла
get_memory_stat_by_column(optimized_dataset)
opt_dtypes = optimized_dataset.dtypes

# 10 колонок
need_column = dict()

optimized_dtypes=optimized_dataset.dtypes
for key in column_names:
    need_column[key] = str(opt_dtypes[key])
    print(f"{key}:{opt_dtypes[key]}")

with open("dtypes.json", "w") as file:
    dtype_json=need_column.copy()
    for key in dtype_json.keys():
        dtype_json[key]=str(dtype_json[key])
    json.dump(dtype_json, file, ensure_ascii=False)

print(need_column)

# Если много данных, можем выборочно держать во временной памяти0
has_header=True
for chunk in pd.read_csv(file_name,
                         usecols=lambda x: x in column_names,
                         dtype=need_column,
                         # parse_dates=['date'],
                         # infer_datetime_format=True,
                         chunksize=50_000):
    print(mem_usage(chunk))
    chunk.to_csv("df.csv", mode="a", header=has_header)
    has_header=False

# #Сортировка
# column_stat_sorted = sorted(column_stat, key=lambda x: x['memory_abs'], reverse=True)
#
# # исправление ошибки с int64
# for column in column_stat_sorted:
#     column['memory_abs'] = int(column['memory_abs'])
#
# output_file = "memory_stats_no_optimization.json"
# with open(output_file, "w", encoding="utf-8") as json_file:
#     json.dump(column_stat_sorted, json_file, ensure_ascii=False)
#
# for dtype in ['float', 'int', 'object']:
#     selected_dtype=df.select_dtypes(include=[dtype])
#     mean_usage_b=selected_dtype.memory_usage(deep=True).mean()
#     mean_usage_mb=mean_usage_b/ 1024**2
#     print("Использование памяти в среднем для {} столбцов: {:03.2f} MB".
#           format(dtype, mean_usage_mb))



converted_obj=pd.DataFrame()
#dow=dataset.day_of_week
#mem_usage(dow)
#opt_dow=dow.astype('category')
print(mem_usage(df))




# Использование памяти
int_types=["uint8", "int8", "int16"]
for it in int_types:
    print(np.iinfo(it))




read_and_optimized=pd.read_csv(file_name,
                               usecols=lambda x: x in column_names,
                               dtype=need_column)
print(read_and_optimized.shape)
print(mem_usage(read_and_optimized))


