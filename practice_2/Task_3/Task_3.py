import json
import msgpack
import numpy as np

# Загрузить данные из JSON файла
with open("products_36.json", "r") as json_file:
    data = json.load(json_file)

# Создать структуру для хранения результатов
result = []

# Обработать каждый товар
for item in data:
    avg_price = item["price"]
    max_price = item["price"]
    min_price = item["price"]

    # Найти среднюю, максимальную и минимальную цены для каждого товара
    for other_item in data:
        if other_item["name"] == item["name"]:
            avg_price = np.mean([avg_price, other_item["price"]])
            max_price = max(max_price, other_item["price"])
            min_price = min(min_price, other_item["price"])

    # Сохранить результаты для каждого товара
    result.append({
        "name": item["name"],
        "avg_price": avg_price,
        "max_price": max_price,
        "min_price": min_price
    })

# Сохранить результаты в JSON
with open("result.json", "w") as json_result_file:
    json.dump(result, json_result_file, indent=2)

# Сохранить результаты в msgpack
with open("result.msgpack", "wb") as msgpack_result_file:
    packed_data = msgpack.packb(result)
    msgpack_result_file.write(packed_data)

# Сравнение размеров файлов
import os
size_json = os.path.getsize('result.json')
size_msgpack = os.path.getsize('result.msgpack')

print(f"Размер файла json: {size_json} байт")
print(f"Размер файла msgpack: {size_msgpack} байт")