import json
import pickle
from bson import json_util
from pymongo import MongoClient

def connect():
    client = MongoClient()
    db = client["test-database"]
    return db.person

def get_from_pkl(filename):
    with open(filename, "rb") as file:
        items = pickle.load(file)
        return items

def insert_many(collection, data):
    collection.insert_many(data)

def write_json(file_name, data):
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(json_util.dumps(data, ensure_ascii=False))

def get_stat_by_salary(collection):
    q = [{
        "$group": {
            "_id": "result",
            "max": {"$max": "$salary"},
            "min": {"$min": "$salary"},
            "avg": {"$avg": "$salary"},
        }
    }]
    items = collection.aggregate(q)
    write_json('result_get_stat_by_salary.json', items)

filename = "task_2_item.pkl"
data = get_from_pkl(filename)
#insert_many(connect(), data)

get_stat_by_salary(connect())



