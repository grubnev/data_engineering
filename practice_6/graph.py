# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import json
import numpy as np
import seaborn as sns
import os

pd.set_option("display.max_rows", 20, "display.max_columns", 60)
# Ноутбук не вывозит рисовку почти никаких графиков(1
def read_file(file_name):
    return pd.read_csv(file_name)

def read_types(file_name):
    dtypes = {}
    with open(file_name, "r") as file:
        dtypes = json.load(file)

    for key in dtypes.keys():
        if dtypes[key] == 'category':
            dtypes[key] = pd.CategoricalDtype
        else:
            dtypes[key] = np.dtype(dtypes[key])

    return dtypes

need_dtypes = read_types("dtypes.json")
dataset = pd.read_csv("df.csv",
                      usecols=lambda x: x in need_dtypes.keys())
#dataset.info(memory_usage='deep')


# plt.figure(figsize=(10, 5))
# plt.pie(dataset['CANCELLATION_REASON'].value_counts(), labels=dataset['CANCELLATION_REASON'].value_counts().index, autopct='%1.1f%%')
# plt.title('Наиболее частые причины отмены рейса')
# plt.axis('equal')
# plt.savefig('pie_chart.png')
#
#
# plt.figure(figsize=(10, 6))
# sns.scatterplot(x="DEPARTURE_DELAY", y="ARRIVAL_DELAY", data=dataset)
# plt.title('Зависимость задержки отправления от задержки прибытия')
# plt.xlabel('Departure Delay')
# plt.ylabel('Arrival Delay')
# plt.savefig('scatter_plot.png')
#
#
# plt.figure(figsize=(10,6))
# sns.barplot(x='DEPARTURE_DELAY', y='AIRLINE', data=dataset)
# plt.title('Авиакомпании самыми сильными задержками в отправлении')
# plt.xlabel('Departure Delay')
# plt.ylabel('Airlines')
# plt.savefig('bar_plot.png')

# top_airports = dataset['DESTINATION_AIRPORT'].value_counts().head(15)
# top_airports_names = top_airports.index
# filtered_dataset = dataset[dataset['DESTINATION_AIRPORT'].isin(top_airports_names)]
#
# plt.figure(figsize=(8, 8))
# sns.countplot(
#     x='DESTINATION_AIRPORT',
#     data=filtered_dataset,
#     order=top_airports_names  )
# plt.title('Топ 15 аэропортов по прибытию')
# plt.xticks(rotation=90)
# plt.savefig('count_plot.png')



plt.figure(figsize=(10, 6))
sns.histplot(dataset['DEPARTURE_DELAY'], bins=50, kde=False)
plt.title('Распределение по опоздания')
plt.xlabel('Departure Delay (minutes)')
plt.ylabel('Frequency')
plt.xlim(-50, 300)
plt.savefig('hist.png')