from bs4 import BeautifulSoup
import json
import numpy as np

def handle_file(file_name):
    items = list()
    with open(file_name, encoding="utf-8") as file:
        text = ""
        for row in file.readlines():
            text += row

        root = BeautifulSoup(text, 'xml')

        for clothing in root.find_all("clothing"):
            item = dict()
            for el in clothing.contents:
                if el.name is None:
                    continue
                elif el.name == "price" or el.name == "reviews":
                    item[el.name] = int(el.get_text().strip())
                elif el.name == "price" or el.name == "rating":
                    item[el.name] = float(el.get_text().strip())
                elif el.name == "new":
                    item[el.name] = el.get_text().strip() == "+"
                elif el.name == "exclusive" or el.name == "sporty":
                    item[el.name] = el.get_text().strip() == "yes"
                else:
                    item[el.name] = el.get_text().strip()

            items.append(item)

    return item


items = []
for i in range(1,101):
    file_name = f"zip_var_36(4)/{i}.xml"
    result = handle_file(file_name)
    items.append(result)

with open("result_all_1.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(items))

#Сортируем по полю rating

items = sorted(items, key=lambda x: x['rating'], reverse=True)

#Определяем количество товаров стоимость которых больше 500 000

filtered_items = []
for item in items:
    if item['price'] > 500000:
        filtered_items.append(item)

print("Колличество всех продуктов", len(items))
print("Колличество отсортированных продуктов", len(filtered_items))

#Статистические характеристики для price

price_array = np.array([item['price'] for item in items])

print("Максимальное значение Price:", np.max(price_array))
print("Минимальное значение Price:", np.min(price_array))
print("Сумма значений Price:", np.sum(price_array))
print("Среднее арифметическое значений Price:", np.mean(price_array))

#Частота меток color

name_array = np.array([item['color'] for item in items])

word_frequency = {}
for word in name_array:
    if word in word_frequency:
        word_frequency[word] += 1
    else:
        word_frequency[word] = 1

sorted_word_frequency = sorted(word_frequency.items(), key=lambda x: x[1], reverse=True)

print(sorted_word_frequency)