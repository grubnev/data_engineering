from bs4 import BeautifulSoup
import json

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
