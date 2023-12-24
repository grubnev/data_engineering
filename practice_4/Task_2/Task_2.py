import sqlite3
import json

def parse_data(file_name):
    items = []
    with open(file_name, "r", encoding="utf-8") as f:
        lines = f.readlines()
        item = dict()
        for line in lines:
            if line == "=====\n":
                items.append(item)
                item = dict()
            else:
                line = line.strip()
                splitted = line.split("::")

                if splitted[0] == "price":
                    item[splitted[0]] = int(splitted[1])
                elif splitted[0] in ["title", "place", "date"]:
                    item[splitted[0]] = splitted[1]
                else:
                    item[splitted[0]] = splitted[1]
    return items

def connect_to_db(db_name):
    connection = sqlite3.connect(db_name)
    connection.row_factory = sqlite3.Row
    return connection

def insert_additional_data(db, data):
    cursor = db.cursor()
    cursor.executemany("""
            INSERT INTO sales (books_id, price, place, date)
            VALUES (
                (SELECT id FROM books WHERE title = :title),
                :price, :place, :date
            )""", data)
    db.commit()

def first_query(db, title):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT * 
        FROM database 
        WHERE books_id = (SELECT id FROM books WHERE title = ?)
        """, [title])
    items = []
    for row in res.fetchall():
        item = dict(row)
        print(item)

    cursor.close()
    return items

def first_query(db, title):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT * 
        FROM sales 
        WHERE books_id = (SELECT id FROM books WHERE title = ?)
        """, [title])
    items = []
    for row in res.fetchall():
        item = dict(row)
        items.append(item)
    cursor.close()
    return items

def second_query(db, title):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT 
            AVG(price) as avg_price, 
            MAX(price) as max_price,
            MIN(price) as min_price
        FROM sales 
        WHERE books_id = (SELECT id FROM books WHERE title = ?)
        """, [title])
    result = dict(res.fetchone())
    cursor.close()
    return result

def third_query(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT title, COUNT(*) as count
        FROM books
        GROUP BY title
        HAVING count > 1
    """,)
    items=[]
    for row in res.fetchall():
        item=dict(row)
        items.append(item)
    cursor.close()
    return items


file_name = "task_2_var_36_subitem.text"
items = parse_data(file_name)
db = connect_to_db('task_2.db')
insert_additional_data(db, items)

# Вся информация по книгам "Прощай, оружие"
result_first_query = first_query(db, "Прощай, оружие")
with open('result_first_query.json', 'w', encoding="utf-8") as f:
    json.dump(result_first_query, f, indent=4, ensure_ascii=False)

#Значения по полю price
result_second_query = second_query(db, "Прощай, оружие")
with open('result_second_query.json', 'w', encoding="utf-8") as f:
    json.dump(result_second_query, f, indent=4, ensure_ascii=False)

#количество книг с одноименным заголовком в таблице
result_third_query = third_query(db)
with open('result_third_query.json', 'w', encoding="utf-8") as f:
    json.dump(result_third_query, f, indent=4, ensure_ascii=False)