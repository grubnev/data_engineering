import sqlite3
import msgpack

def parse_data(file_name):
    items= []
    with open(file_name, 'r', encoding='utf-8') as f:
        data = msgpack.unpack(file, raw=False)

        print(data)


    return items

def connect_to_db(file_name):
    connection = sqlite3.connect(file_name)
    connection.row_factory = sqlite3.Row
    return connection

def insert_data(db, data):
    cursor = db.cursor()

    cursor.executemany("""
        INSERT INTO books (title, author, genre, pages, published_year, isbn, rating, views)
        VALUES ()
        """, data)
    db.commit()

def get_top_by_views(db, limit):
    cursor = db.cursor()
    res = cursor.execute("SELECT * FROM books ORDER BY views DESC LIMIT ?", [limit])
    items = []
    for row in res.fetchall():
        item = dict(row)
        print(item)

    cursor.close()
    return items



file_name = 'task_1_var_36_item.msgpack'
parse_data(file_name)