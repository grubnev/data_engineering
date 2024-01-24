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
                      usecols=lambda x: x in need_dtypes.keys(),
                      dtype=need_dtypes,
                      parse_dates=['date'])
#dataset.info(memory_usage='deep')


plt.figure(figsize=(10,5))
plt.ticklabel_format(style='plain')
plt.plot(dataset.groupby(["day_of_week"])['length_minutes'].sum().values, marker='.',)
plt.title('Продолжительность игр по дням недели')
plt.xlabel('День недели')
plt.ylabel('Продолжительность')
plt.savefig('linear.png')


plt.figure(figsize=(10, 5))
sns.barplot(x='day_of_week', y='number_of_game', data=dataset, errorbar=None)
plt.title('Количество игр по дням недели')
plt.xlabel('День недели')
plt.ylabel('Количество игр')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('bar_plot.png')


plt.figure(figsize=(10, 10))
sns.heatmap(dataset[['v_hits', 'h_hits', 'h_walks', 'h_errors']], cmap='coolwarm')
plt.title('Heatmap по статистике игр')
plt.xlabel('Home команда')
plt.ylabel('Visitor команда')
plt.tight_layout()
plt.savefig('heatmap.png')

plt.figure(figsize=(10, 6))
plt.scatter(dataset['h_hits'], dataset['v_hits'])
plt.title('Home Hits vs Visitor Hits')
plt.xlabel('Home Hits')
plt.ylabel('Visitor Hits')
plt.tight_layout()
plt.savefig('scatter_plot.png')

plt.figure(figsize=(6, 6))
plt.pie(dataset['day_of_week'].value_counts(), labels=dataset['day_of_week'].unique(), autopct='%1.1f%%')
plt.title('Распределение по дням недели')
plt.axis('equal')
plt.savefig('pie_chart.png')



plt.show()