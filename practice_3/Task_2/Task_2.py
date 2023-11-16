from bs4 import BeautifulSoup
import numpy as np
import re
import json

def handle_file(file_name):
    items = list()
    with open(file_name, encoding="utf-8") as file:
        text = ""
        for row in file.readlines():
            text += row

        site = BeautifulSoup(text, 'html.parser')
        products = site.find_all("div", attrs={'class': 'product-item'})

        for product in products:
            item = dict()
            item['id'] = product.a['data-id']
            item['link'] = product.find_all('a')[1]['href']
            item['img_url'] = product.find_all("img")[0]['src']
            item['title'] = product.find_all("span")[0].get_text().strip()
            item['price'] = int(product.price.get_text().replace("₽", "").replace(" ","").strip())
            item['bonus'] = int(product.strong.get_text().replace("+ начислим ", "").replace(" бонусов", "").strip())
            props = product.ul.find_all("li")
            for prop in props:
                item[prop['type']] = prop.get_text().strip()

            items.append(item)
    return items

items = []
for i in range(1, 41):
    file_name = f"zip_var_36(2)/{i}.html"
    items += handle_file(file_name)

items = sorted(items, key=lambda x: x['price'], reverse=True)

#Определяем количество продуктов стоимость которых больше 100 000р
filtered_items = []
for product in items:
    if product['price'] > 100000:
        filtered_items.append(product)

print("Колличество всех продуктов", len(items))
print("Колличество отсортированных продуктов", len(filtered_items))

with open("result_filtred_1.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(filtered_items))

with open("result_all_1.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(items))

price_array = np.array([items['price'] for item in items])

print("Максимальное значение Price:", np.max(price_array))
print("Минимальное значение Price:", np.min(price_array))
print("Сумма значений Price:", np.sum(price_array))
print("Среднее арифметическое значений Price:", np.mean(price_array))

title_array = np.array([items['title'] for item in items])

word_frequency = {}
for word in title_array:
    if word in word_frequency:
        word_frequency[word] += 1
    else:
        word_frequency[word] = 1

sorted_word_frequency = sorted(word_frequency.items(), key=lambda x: x[1], reverse=True)

print(sorted_word_frequency)
