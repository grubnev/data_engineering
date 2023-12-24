import sqlite3
import msgpack

def parse_data(file_name):
    with open(file_name, 'rb') as f:
        data = msgpack.unpack(f, raw=False)
    return data

def connect_to_db(db_name):
    connection = sqlite3.connect(db_name)
    connection.row_factory = sqlite3.Row
    return connection

def create_table(db):
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            author TEXT,
            genre TEXT,
            pages INTEGER,
            published_year INTEGER,
            isbn TEXT,
            rating REAL,
            views INTEGER
        )
    ''')
    db.commit()

def insert_data(db, data):
    cursor = db.cursor()
    cursor.executemany('''
        INSERT INTO books (title, author, genre, pages, published_year, isbn, rating, views)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', [(item['title'], item['author'], item['genre'], item['pages'], item['published_year'],
           item['isbn'], item['rating'], item['views']) for item in data])
    db.commit()

def get_top_by_views(db, limit):
    cursor = db.cursor()
    res = cursor.execute("SELECT * FROM books ORDER BY views DESC LIMIT ?", [limit])
    items = [dict(row) for row in res.fetchall()]
    return items

if __name__ == "__main__":
    file_name = 'task_1_var_36_item.msgpack'
    data = parse_data(file_name)

    db_name = 'books_database.db'
    connection = connect_to_db(db_name)
    create_table(connection)
    insert_data(connection, data)

    top_books = get_top_by_views(connection, 2)
    print(top_books)

    connection.close()