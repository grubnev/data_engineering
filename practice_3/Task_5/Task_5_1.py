from bs4 import BeautifulSoup
import numpy as np
import re
import json

def handle_file(file_name):

    with open(file_name, encoding="utf-8") as file:
        text = ""
        for row in file.readlines():
            text += row

        site = BeautifulSoup(text, 'html.parser')
        parameters = site.find_all('div', attrs={"class":"row"})

        item = dict()
        item['title'] = site.find_all('h1')[0].get_text()
        item['price'] = int(site.find_all('span', attrs={"itemprop": "price"})[0].get_text())

        return item

items = []
for i in range(1, 26):
    file_name = f"1/{i}.html"
    result = handle_file(file_name)
    items.append(result)

# Сортировка по views

items = sorted(items, key=lambda x: x['price'], reverse=True)

with open("result_all_5.1.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(items))

# Определяем количество строений рейтинг которых больше 2

filtered_items = []
for building in items:
    if building['price'] > 1000:
        filtered_items.append((building))

print("Всего элементов:", len(items))
print("Фильтрация элементов:", len(filtered_items))

# Статистические характеристики для views

views_array = np.array([item['price'] for item in items])

print("Максимальное значение Views:", np.max(views_array))
print("Минимальное значение Views:", np.min(views_array))
print("Сумма значений Views:", np.sum(views_array))
print("Среднее арифметическое значений Views:", np.mean(views_array))

# Частота меток city

city_array = np.array([item['price'] for item in items])

word_frequency = {}
for word in city_array:
    if word in word_frequency:
        word_frequency[word] += 1
    else:
        word_frequency[word] = 1

sorted_word_frequency = sorted(word_frequency.items(), key=lambda x: x[1], reverse=True)

print(sorted_word_frequency)