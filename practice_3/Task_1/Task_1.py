from bs4 import BeautifulSoup
import numpy as np
import re
import json


def handle_file(file_name):
    with open(file_name, encoding='utf-8') as file:
        text = ""
        for row in file.readlines():
            text += row

        site = BeautifulSoup(text, 'html.parser')

        item = dict()
        item['city'] = site.find_all("span", string=re.compile("Город:"))[0].get_text().replace("Город:", "").strip()
        item['build'] = site.find_all("h1")[0].get_text().replace("Строение:","").strip()
        address = site.find_all("p", attrs={"class": "address-p"})[0].get_text().split("Индекс:")
        item['address'] = address[0].replace("Улица:","").strip()
        item['index'] = address[1].strip()
        item['floors'] = int(site.find_all("span", attrs={"class": "floors"})[0].get_text().split(":")[1].strip())
        item['year'] = int(site.find_all("span", attrs={"class": "year"})[0].get_text().split(":")[0].replace("Построено в", "").strip())
        item['parking'] = site.find_all("span", string=re.compile("Парковка:"))[0].get_text().replace("Парковка:", "").strip()
        item['parking'] = item["parking"] == 'есть'
        item['img'] = site.find_all("img")[0]['src']
        item['rating'] = float(site.find_all("span", string=re.compile("Рейтинг:"))[0].get_text().split(":")[1].strip())
        item['views'] = int(site.find_all("span", string=re.compile("Просмотры:"))[0].get_text().split(":")[1].strip())

        return item

items = []
for i in range(1,1000):
    file_name = f"zip_var_36(1)/{i}.html"
    result = handle_file(file_name)
    items.append(result)

#Сортировка по views

items = sorted(items, key=lambda x: x['views'], reverse = True)

with open("result_all_1.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(items, ensure_ascii=False))

#Определяем количество строений рейтинг которых больше 2

filtered_items = []
for building in items:
    if building['rating'] >= 2:
        filtered_items.append((building))

print("Всего элементов:", len(items))
print("Фильтрация элементов:", len(filtered_items))

#Статистические характеристики для views

views_array = np.array([item['views'] for item in items])

views_stats = {
    "max_views": int(np.max(views_array)),
    "min_views": int(np.min(views_array)),
    "sum_views": int(np.sum(views_array)),
    "mean_views": int(np.mean(views_array))
}

with open('views_stats_1.json', 'w', encoding="utf-8") as f:
    json.dump(views_stats, f, indent=4, ensure_ascii=False)

#Частота меток city

city_array = np.array([item['city'] for item in items])

word_frequency = {}
for word in city_array:
    if word in word_frequency:
        word_frequency[word] += 1
    else:
        word_frequency[word] = 1

sorted_word_frequency = sorted(word_frequency.items(), key=lambda x: x[1], reverse=True)

with open("sorted_word_frequency_1.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(sorted_word_frequency, ensure_ascii=False))

print(sorted_word_frequency)

