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

def get_freq_by_job(collection):
    q = [{
        "$group": {
            "_id": "$job",
            "count": {"$sum": 1}
        }
    },
    {
        "$sort": {
            "count": -1
        }
    }]
    items = collection.aggregate(q)
    write_json('result_get_freq_by_job.json', items)

def get_salary_stat_by_column(collection, column_name):
    q = [{
        "$group":{
            "_id": f"${column_name}",
            "max": {"$max": "$salary"},
            "min": {"$min": "$salary"},
            "avg": {"$avg": "$salary"},
        }
    }]
    items = collection.aggregate(q)
    write_json(f'result_get_salary_stat_by_{column_name}.json', items)

def get_age_stat_by_column(collection, column_name):
    q = [{
        "$group": {
            "_id": f"${column_name}",
            "max": {"$max": "$age"},
            "min": {"$min": "$age"},
            "avg": {"$avg": "$age"},
        }
    }]
    items = collection.aggregate(q)
    write_json(f'result_get_age_stat_by_{column_name}.json', items)

def max_salary_by_min_age_match(collection):
    q = [{
        "$match": {
            "age": 18
        }
    },
    {
        "$group": {
            "_id": "result",
            "min_age": {"$min": "$age"},
            "max_salary": {"$max": "$salary"}
        }
    }]
    items = collection.aggregate(q)
    write_json('result_max_salary_by_min_age_match.json', items)


def min_salary_by_max_age(collection):
    q = [{
        "$group": {
            "_id": "$age",
            "min_salary": {"$min": "$salary"}
        }
    },
        {
            "$group": {
                "_id": "result",
                "max_age": {"$max": "$_id"},
                "min_salary": {"$min": "$min_salary"}
            }
        }]
    items = collection.aggregate(q)
    write_json('result_min_salary_by_max_age.json', items)

def big_query(collection):
    q = [{
            "$match": {
                "salary": {"$gt": 50_000}
            },
        },
        {
            "$group": {
                "_id": "$city",
                "min": {"$min": "$age"},
                "max": {"$max": "$age"},
                "avg": {"$avg": "$age"},
            }
        },
        {
            "$sort": {
                "avg": -1
            }
        }
    ]
    items = collection.aggregate(q)
    write_json('result_big_query.json', items)

def big_query_2(collection):
    items = []
    q = [
        {
            "$match": {
                "city": {"$in": ["Хихон", "Ереван", "Афины", "Загреб"]},
                "job": {"$in": ["Врач", "Повар", "Учитель", "Инженер"]},
                "$or": [
                    {"age": {"$gt": 18, "$lt": 25}},
                    {"age": {"$gt": 50, "$lt": 65}},
                ]
            }
        },
        {"$group": {
            "_id": "result",
            "max": {"$max": "$salary"},
            "min": {"$min": "$salary"},
            "avg": {"$avg": "$salary"}
        }
        }
    ]
    items = collection.aggregate(q)
    write_json('result_big_query_2.json', items)


filename = "task_2_item.pkl"
data = get_from_pkl(filename)
#insert_many(connect(), data)

get_stat_by_salary(connect())
get_freq_by_job(connect())
get_salary_stat_by_column(connect(), "city")
get_salary_stat_by_column(connect(), "job")
get_age_stat_by_column(connect(), "city")
get_age_stat_by_column(connect(), "job")
max_salary_by_min_age_match(connect())
min_salary_by_max_age(connect())
big_query(connect())
big_query_2(connect())



