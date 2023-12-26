import json
from bson import json_util
from pymongo import MongoClient

def connect():
    client = MongoClient()
    db = client["test-database"]
    return db.person

def get_from_json(filename):
    items = []
    with open(filename, "r", encoding="utf-8") as f:
        items = json.load(f)
    return items

def insert_many(collection, data):
    collection.insert_many(data)

def write_json(file_name, data):
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(json_util.dumps(data, ensure_ascii=False))

def sort_by_salary(collection):
        items = collection.find().limit(10).sort('salary', -1)
        write_json('result_sort_by_salary.json', items)

def filtred_by_age(collection):
    cursor = collection.find({"age":{"$lt":30}}, limit = 15).sort({"salary": -1})
    items = list(cursor)  # Convert cursor to list
    write_json('result_filter_by_age.json', items)

def complex_filter_by_city_and_job(collection):
    cursor = collection.find({"city": "Душанбе", "job": {"$in": ["Продавец", "Программист", "Учитель"]}}, limit = 10).sort({"age":1})
    items = list(cursor)  # Convert cursor to list
    write_json('result_complex_filter_by_city_and_job.json', items)

def count_obj(collection):
    items = collection.count_documents({
        "$and": [
            {"age": {"$gte": 18, "$lte": 65}},
            {"year": {"$in": [2019, 2020, 2021, 2022]}},
            {"$or": [
                {"salary": {"$gt": 50000, "$lte": 75000}},
                {"salary": {"$gt": 125000, "$lt": 150000}}
            ]}
        ]
    })
    write_json('result_count_obj.json', items)


filename = "task_1_item.json"
data = get_from_json(filename)
#insert_many(connect(), data)

sort_by_salary(connect())
filtred_by_age(connect())
complex_filter_by_city_and_job(connect())
count_obj(connect())
