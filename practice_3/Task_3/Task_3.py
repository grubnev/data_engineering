from bs4 import BeautifulSoup
import json

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
        item['radius'] = star.find_all("radius")[0].get_text().strip()
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
    f.write(json.dumps(items))