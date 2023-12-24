from bs4 import BeautifulSoup
import json
import numpy as np

def handle_file(file_name):
    with open(file_name, encoding='utf-8') as file:
        text = ""
        for row in file.readlines():
            text += row

        star = BeautifulSoup(text, 'xml')

        item = dict()
        item['name'] = star.find_all("name")[0].get_text().strip()
        item['constellation'] = star.find_all("constellation")[0].get_text().strip()
        item['spectral-class'] = star.find_all("spectral-class")[0].get_text().strip()
        item['radius'] = int(star.find_all("radius")[0].get_text().strip())
        item['age'] = star.find_all("distance")[0].get_text().strip()
        item['distance'] = star.find_all("distance")[0].get_text().strip()
        item['absolute-magnitude'] = star.find_all("absolute-magnitude")[0].get_text().strip()

        return item

items = []
for i in range(1,501):
    file_name = f"zip_var_36(3)/{i}.xml"
    result = handle_file(file_name)
    items.append(result)

with open("result_all_3.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(items, ensure_ascii=False))

#Сортировка по spectral-class

items = sorted(items, key=lambda x: x['spectral-class'], reverse=True)

#Определяем количество звезд радиус которых больше 900 000 000
filtered_items = []
for star in items:
    if star['radius'] > 900000000:
        filtered_items.append(star)

print("Колличество всех продуктов", len(items))
print("Колличество отсортированных продуктов", len(filtered_items))

#Статистические характеристики для radius

radius_array = np.array([item['radius'] for item in items])

print("Максимальное значение Radius:", np.max(radius_array))
print("Минимальное значение Radius:", np.min(radius_array))
print("Сумма значений Radius:", np.sum(radius_array))
print("Среднее арифметическое значений Radius:", np.mean(radius_array))

#Частота меток spectral-class

name_array = np.array([item['spectral-class'] for item in items])

word_frequency = {}
for word in name_array:
    if word in word_frequency:
        word_frequency[word] += 1
    else:
        word_frequency[word] = 1

sorted_word_frequency = sorted(word_frequency.items(), key=lambda x: x[1], reverse=True)

print(sorted_word_frequency)