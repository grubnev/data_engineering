import sqlite3
import msgpack
import json

def parse_data(file_name):
    with open(file_name, 'rb') as f:
        items = msgpack.unpack(f, raw=False)
    return items

def connect_to_db(db_name):
    connection = sqlite3.connect(db_name)
    connection.row_factory = sqlite3.Row
    return connection

def insert_data(db, data):
    cursor = db.cursor()
    cursor.executemany('''
        INSERT INTO books (title, author, genre, pages, published_year, isbn, rating, views)
        VALUES(:title, :author, :genre, :pages, :published_year, :isbn, :rating, :views)
        ''', data)
    db.commit()

def get_top_by_views(db, limit):
    cursor = db.cursor()
    res = cursor.execute("SELECT title, author, pages, views FROM books ORDER BY views DESC LIMIT ?", [limit])
    items = []
    for row in res.fetchall():
        item = dict(row)
        items.append(item)
    cursor.close()
    return items

def get_stat_by_pages(db):
    cursor = db.cursor()
    res = cursor.execute("""
        select
            sum(pages) as sum,
            avg(pages) as avg,
            min(pages) as min,
            max(pages) as max
        from books
        """)
    result = dict(res.fetchone())
    cursor.close()
    with open('result_get_stat_by_pages_1.json', 'w', encoding="utf-8") as f:
        json.dump(result, f, indent=4, ensure_ascii=False)

def get_freq_by_century(db):
    cursor=db.cursor()
    res=cursor.execute("""
            SELECT
                CAST(count(*)as REAL)/ (SELECT COUNT(*) FROM books) as count,
                (FLOOR (published_year/100)+1) as century
            FROM books
            GROUP BY (FLOOR(published_year/100)+1)
            """)
    result=[]
    for row in res.fetchall():
        item = dict(row)
        result.append(item)
    cursor.close()
    with open('result_get_freq_by_century_1.json', 'w', encoding="utf-8") as f:
        json.dump(result, f, indent=4, ensure_ascii=False)
    return result

def filter_by_published_year(db,min_published_year, limit=46):
    cursor=db.cursor()
    res=cursor.execute("""
            SELECT *
            FROM books
            WHERE published_year > ?
            ORDER BY views DESC
            LIMIT ?
            """, [min_published_year, limit])
    result = []
    for row in res.fetchall():
        item = dict(row)
        result.append(item)
    cursor.close()
    return result


file_name = 'task_1_var_36_item.msgpack'
data = parse_data(file_name)
db = connect_to_db('task_1.db')
#insert_data(db, data)

# вывод первых 46 отсортированных строк по году в json
result_get_top_by_views = get_top_by_views(db, 46)
with open('result_get_top_by_views_1.json', 'w', encoding="utf-8") as f:
    json.dump(result_get_top_by_views, f, indent=4, ensure_ascii=False)

# вывод (сумму, мин, макс, среднее) по произвольному числовому полю;
result_get_stat_by_pages = get_stat_by_pages(db)

# вывод частоты встречаемости для категориального поля
result_get_freq_by_century = get_freq_by_century(db)

# вывод 46 отфильтрованных по произвольному предикату отсортированных по произвольному числовому полю строк из таблицы в json
result_filter_by_published_year = filter_by_published_year(db, 46)
with open('result_filter_by_published_year_1.json', 'w', encoding="utf-8") as f:
    json.dump(result_filter_by_published_year, f, indent=4, ensure_ascii=False)