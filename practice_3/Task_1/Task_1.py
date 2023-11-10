from bs4 import BeautifulSoup
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

        print(item)
        return item

items = []
for i in range(1,999):
    file_name = f"zip_var_36(1)/{i}.html"
    result = handle_file(file_name)
    items.append(result)

items = sorted(items, key=lambda x: x['views'], reverse = True)

with open("result_all_1.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(items))

filtered_items = []
for building in items:
    if building['rating'] >= 2:
        filtered_items.append((building))

print(len(items))
print(len(filtered_items))