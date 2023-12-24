import sqlite3
import msgpack
import pickle
import json

def load_pkl_data(file_name):
    with open(file_name, 'rb') as f:
        data = pickle.load(f)
    items = []
    for item in data:
        del item['energy'], item['popularity']
        items.append(item)
    return items

def lead_msgpack_data(file_name):
    with open(file_name, 'rb') as f:
        data = msgpack.load(f)
    items = []
    for item in data:
        del item['mode'], item['speechiness'], item['instrumentalness']
        items.append(item)
    return items

def insert_pkl_data(db, data):
    cursor = db.cursor()
    cursor.executemany("""
            insert into music (artist, song, duration_ms, year, tempo, genre, acousticness)
            values (
                :artist, :song, :duration_ms, :year, :tempo, :genre, :acousticness
            )""", data)
    db.commit()

def insert_msgpack_data(db, data):
    cursor = db.cursor()
    cursor.executemany("""
            insert into music (artist, song, duration_ms, year, tempo, genre, acousticness)
            values (
                :artist, :song, :duration_ms, :year, :tempo, :genre, :acousticness
            )""", data)
    db.commit()

def get_top_by_views(db, limit):
    cursor = db.cursor()
    res = cursor.execute("SELECT artist, song, duration_ms, year, tempo, genre, acousticness FROM music ORDER BY year DESC LIMIT ?", [limit])
    items = []
    for row in res.fetchall():
        item = {'artist': row[0], 'song': row[1],'duration_ms': row[2], 'year': row[3],'tempo': row[4], 'genre': row[5],'acousticness': row[6]}
        items.append(item)
    cursor.close()
    return items

def get_stat_by_pages(db):
    cursor = db.cursor()
    res = cursor.execute("""
        select
            sum(duration_ms) as sum,
            avg(duration_ms) as avg,
            min(duration_ms) as min,
            max(duration_ms) as max
        from music
        """)
    result = res.fetchone()
    cursor.close()
    with open('result_get_stat_by_pages_3.json', 'w', encoding="utf-8") as f:
        json.dump(result, f, indent=4, ensure_ascii=False)

def get_freq_by_century(db):
    cursor=db.cursor()
    res=cursor.execute("""
            SELECT
                CAST(count(*)as REAL)/ (SELECT COUNT(*) FROM music) as count,
                (FLOOR (year/100)+1) as century
            FROM music
            GROUP BY (FLOOR(year/100)+1)
            """)
    result=[]
    for row in res.fetchall():
        item = {'count': row[0], 'century': row[1]}
        result.append(item)
    cursor.close()
    with open('result_get_freq_by_century_3.json', 'w', encoding="utf-8") as f:
        json.dump(result, f, indent=4, ensure_ascii=False)
    return result

def filter_by_published_year(db, min_year, limit=46):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT *
        FROM music
        WHERE year > ?
        ORDER BY duration_ms DESC
        LIMIT ?
    """, [min_year, limit])
    result = []
    column_names = [description[0] for description in res.description]
    for row in res.fetchall():
        item = {column_names[i]: row[i] for i in range(len(column_names))}
        result.append(item)
    cursor.close()
    return result

file_name_1 = 'task_3_var_36_part_1.pkl'
file_name_2 = 'task_3_var_36_part_2.msgpack'

print(load_pkl_data(file_name_1)[0].keys())
print(lead_msgpack_data(file_name_2)[0].keys())

items_1 = load_pkl_data(file_name_1)
items_2 = lead_msgpack_data(file_name_2)

db = sqlite3.connect('Task_3.db')
c = db.cursor()

#insert_pkl_data(db, items_1)
#insert_msgpack_data(db, items_2)

# вывод первых 36+10 отсортированных строк из таблицы в json
result_get_top_by_views = get_top_by_views(db, 46)
with open('result_get_top_by_views_3.json', 'w', encoding="utf-8") as f:
    json.dump(result_get_top_by_views, f, indent=4, ensure_ascii=False)

# вывод (сумму, мин, макс, среднее) по произвольному числовому полю;
result_get_stat_by_pages = get_stat_by_pages(db)

# вывод частоты встречаемости для категориального поля
result_get_freq_by_century = get_freq_by_century(db)

# вывод 46 отфильтрованных по произвольному предикату отсортированных по произвольному числовому полю строк из таблицы в json
result_filter_by_published_year = filter_by_published_year(db, 46)
with open('result_filter_by_published_year_3.json', 'w', encoding="utf-8") as f:
    json.dump(result_filter_by_published_year, f, indent=4, ensure_ascii=False)