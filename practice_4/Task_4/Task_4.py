import sqlite3
import pickle
import csv
import json

def load_pkl_data(file_name):
    with open(file_name, 'rb') as f:
        data = pickle.load(f)
    items = []
    for item in data:
        if len(item) == 6:
            item['category'] = 'no'
        item['version'] = 0
        items.append(item)
    return items

def load_csv_data(file_name):
    items = []
    with open(file_name, "r", encoding="utf-8") as input:
        reader = csv.reader(input, delimiter=";")
        next(reader)
        for row in reader:
            if len(row) == 0:
                continue
            item = dict()
            item['name'] = row[0]
            item['method'] = row[1]
            if item['method'] == 'available':
                item['param'] = row[2] == "True"
            elif item['method'] != 'remove':
                item['param'] = float(row[2])
            items.append(item)
    return items

def insert_pkl_data(db, data):
    cursor = db.cursor()
    print(data)
    cursor.executemany("""
            insert into products (name, price, quantity, category, fromCity, isAvailable, views, version)
            values (
                :name, :price, :quantity, :category, :fromCity, :isAvailable, :views, :version
            )""", data)
    db.commit()

def delete_by_name(db, name):
    cursor = db.cursor()
    cursor.execute("DELETE FROM products WHERE name = ?", [name])
    db.commit()


def update_price_by_percent(db, name, percent):
    cursor = db.cursor()
    cursor.execute("UPDATE products SET price = round(price * (1 + ?), 2) WHERE name = ?", [percent, name])
    cursor.execute("UPDATE products SET version = version + 1 WHERE name = ?", [name])
    db.commit()


def update_price(db, name, param):
    cursor = db.cursor()
    res = cursor.execute("""
     UPDATE products SET price = (price + ?) WHERE (name = ?) AND ((price + ?) > 0)
     """, [param, name, param])
    if res.rowcount > 0:
        cursor.execute("UPDATE products SET version = version + 1 WHERE name = ?", [name])
        db.commit()


def update_available(db, name, param):
    cursor = db.cursor()
    cursor.execute("UPDATE products SET isavailable = ? WHERE name = ?", [param, name])
    cursor.execute("UPDATE products SET version = version + 1 WHERE name = ?", [name])
    db.commit()


def update_quantity(db, name, param):
    cursor = db.cursor()
    res = cursor.execute("UPDATE products SET quantity = (quantity + ?) WHERE (name = ?) AND ((quantity + ?) > 0)",
                         [param, name, param])
    if res.rowcount > 0:
        cursor.execute("UPDATE products SET version = version + 1 WHERE name = ?", [name])
        db.commit()


def handle_update(db, update_items):
    for item in update_items:
        match item['method']:
            case 'remove':
                pass
                print(f"Deleting {item['name']}")
                delete_by_name(db, item['name'])
            case 'price_percent':
                print(f"Update price by percent for {item['name']}")
                update_price_by_percent(db, item['name'], item['param'])
            case 'price_abs':
                print(f"Update price absolute value for {item['name']}")
                update_price(db, item['name'], item['param'])
            case 'quantity_sub':
                print(f"Subtract quantity for {item['name']}")
                update_quantity(db, item['name'], item['param'])
            case 'quantity_add':
                print(f"Add quantity for {item['name']}")
                update_quantity(db, item['name'], item['param'])
            case 'available':
                print(f"Update availability for {item['name']}")
                update_available(db, item['name'], item['param'])

def top_10(db, limit):
    cursor=db.cursor()
    res = cursor.execute("SELECT name, version FROM products ORDER BY version DESC LIMIT ?", [limit])
    items = []
    for row in res.fetchall():
        item = {'name': row[0], 'version': row[1]}
        items.append(item)
    cursor.close()
    return items

def price_analysis(db):
    cursor = db.cursor()
    res = cursor.execute("""
            SELECT category,
                ROUND(SUM(price), 2) as sum, 
                ROUND(AVG(price), 2) as avg, 
                MIN(price) as min,
                MAX(price) as max,
                COUNT (*) as count
            FROM products
            GROUP BY category
            """)
    items = []
    for row in res.fetchall():
        item = {'category': row[0], 'sum': row[1], 'avg': row[2], 'min': row[3], 'max': row[4], 'count': row[5]}
        items.append(item)
    cursor.close()
    return items

def analyse_quant(db):
    cursor=db.cursor()
    res=cursor.execute("""
            SELECT category,
                SUM(quantity) as quantity
            FROM products
            GROUP BY category
            """)
    items = []
    for row in res.fetchall():
        item={'category': row[0], 'sum': row[1]}
        items.append(item)
    cursor.close()
    return items

def available(db, categories):
    cursor = db.cursor()
    result = {}
    for category in categories:
        res = cursor.execute("""
            SELECT name, price
            FROM products
            WHERE category = ? AND isavailable = 1
            ORDER BY price
        """, [category])
        result[category] = {row[0]: row[1] for row in res.fetchall()}
    cursor.close()
    return result


file_name_1 = 'task_4_var_36_product_data.pkl'
file_name_2 = 'task_4_var_36_update_data.csv'

items_1 = load_pkl_data(file_name_1)
items_2 = load_csv_data(file_name_2)

db = sqlite3.connect('Task_4.db')

#добавление данных в БД
#insert_pkl_data(db, items_1)

#обновление даных в БД
#handle_update(db, items_2)

# Топ 10 обновляемых товаров
result_task_1 = top_10(db,10)
with open('result_task_4.1.json', 'w', encoding="utf-8") as f:
    json.dump(result_task_1, f, indent=4)

# Анализ цен товаров, найдя (сумму, мин, макс, среднее) для каждой группы, количество товаров в группе
result_task_2=price_analysis(db)
with open('result_task_4.2.json', 'w') as f:
    json.dump(result_task_2, f, indent=4)

# анализ остатков товаров, (сумму, мин, макс, среднее) для каждой группы товаров
result_task_3=analyse_quant(db)
with open('result_task_4.3.json', 'w') as f:
    json.dump(result_task_3, f, indent=4)

# Самый дешевый товар в наличии в каждой категории
categories = ["cosmetics", "fruit", "tools"]
result_task_4 = available(db, categories)
with open('result_task_4.4.json', 'w') as f:
    json.dump(result_task_4, f, indent=4)

