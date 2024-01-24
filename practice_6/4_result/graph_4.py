# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import json
import numpy as np
import seaborn as sns
import os

pd.set_option("display.max_rows", 20, "display.max_columns", 60)

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
                      # dtype=need_dtypes,
                      # parse_dates=['date']
#dataset.info(memory_usage='deep')

plt.figure(figsize=(8, 8))
sns.countplot(x='premium', data=dataset)
plt.title('Premium Distribution')
plt.savefig('bar_chart.png')

plt.figure(figsize=(10, 5))
plt.ticklabel_format(style='plain')
plt.plot(dataset['salary_from'], label='Salary From')
plt.plot(dataset['salary_to'], label='Salary To')
plt.xlabel('Number of Records')
plt.ylabel('Salary')
plt.title('Распределение зарплат')
plt.legend()
plt.savefig('line_chart.png')


plt.figure(figsize=(10,6))
sns.scatterplot(data=dataset, x='employer_id', y='salary_from')
plt.title('Связь между количеством сотрудников и зарплатой')
plt.savefig('scatter_plot.png')


plt.figure(figsize=(6, 6))
plt.pie(dataset['schedule_name'].value_counts(), labels=dataset['schedule_name'].unique(), autopct='%1.1f%%')
plt.title('Форма работы')
plt.axis('equal')
plt.savefig('pie_chart.png')



# Drop the 'schedule_name' column
dataset_no_schedule = dataset.drop(columns=['schedule_name'])

# Create the heatmap with the updated dataset
plt.figure(figsize=(10, 8))
sns.heatmap(dataset_no_schedule.corr(), annot=True, fmt=".2f")
plt.title('Матрица корреляции')
plt.savefig('correlation.png')

plt.show()