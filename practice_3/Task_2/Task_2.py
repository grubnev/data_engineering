from bs4 import BeautifulSoup
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
for i in range(1, 40):
    file_name = f"zip_var_36(2)/{i}.html"
    items += handle_file(file_name)

items = sorted(items, key=lambda x: x['price'], reverse=True)

#Определяем количество продуктов стоимость которых больше 100 000р
filtered_items = []
for product in items:
    if product['price'] > 100000:
        filtered_items.append(product)

print(len(items))
print(len(filtered_items))

with open("result_filtred_1.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(filtered_items))

with open("result_all_1.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(items))
