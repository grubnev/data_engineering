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
        products = site.find_all("div", attrs={'class': 'page-shop'}) + site.find_all("div", attrs={'class': 'block loaded visible'}) + site.find_all("div", attrs={'class': 'block visible'})
        item = dict()
        for product in products:
            item['title'] = product.find_all("a")[0].get_text().strip()
            item['price'] = int(product.find_all("div", attrs={'class': 'price'})[0].get_text().replace(" Р.", "").strip())
            item['delivery'] = product.find_all("div", attrs={'class': 'delivery'})[0].get_text().replace('<span class="icon-truck"></span>', "").strip()

            items.append(item)
    return item

items = []
for i in range(1, 6):
    file_name = f"2/{i}.html"
    result = handle_file(file_name)
    items.append(result)
del items[-1]

#Сортировка по price

items = sorted(items, key=lambda x: x['price'], reverse=True)

#Определяем количество продуктов стоимость которых больше 500р
filtered_items = []
for product in items:
    if product['price'] > 500:
        filtered_items.append(product)

print("Колличество всех продуктов", len(items))
print("Колличество отсортированных продуктов", len(filtered_items))

with open("result_filtred_5.2.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(filtered_items))

with open("result_all_5.2.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(items))

#Статистические характеристики для radius

price_array = np.array([item['price'] for item in items])

print("Максимальное значение Price:", np.max(price_array))
print("Минимальное значение Price:", np.min(price_array))
print("Сумма значений Price:", np.sum(price_array))
print("Среднее арифметическое значений Price:", np.mean(price_array))
