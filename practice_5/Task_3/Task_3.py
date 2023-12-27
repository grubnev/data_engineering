import json
from bson import json_util
from pymongo import MongoClient

def connect():
    client = MongoClient()
    db = client["test-database"]
    return db.person

def get_from_text(file_name):
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
                if len(splitted) == 2:
                    if splitted[0] in ['id', 'year', 'age']:
                        item[splitted[0]] = int(splitted[1])
                    elif splitted[0] == 'salary':
                        item[splitted[0]] = float(splitted[1])
                    else:
                        item[splitted[0]] = splitted[1]
    return items

def insert_many(collection, data):
    collection.insert_many(data)

def write_json(file_name, data):
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(json_util.dumps(data, ensure_ascii=False))

def delete_salary(collection):
    result=collection.delete_many({
        "$or": [
            {"salary": {"$lt":25_000}},
            {"salary": {"$gt": 175_000}},
        ]
    })
    print(result)

def update_age(collection):
    result=collection.update_many({}, {
        "$inc":{
            "age":1}
    })
    print(result)

def increase_salary_by_job(collection):
    filter={
        "job":{"$in":["Учитель", "Врач","Строитель","Повар"]}
    }
    update={
        "$mul": {
            "salary": 1.05
        }
    }
    result=collection.update_many(filter, update)
    print(result)

def increase_salary_by_city(collection):
    filter={
        "city":{"$in":["Баку", "Луго","Эльче","Душанбе"]}
    }
    update={
        "$mul": {
            "salary": 1.07
        }
    }
    result=collection.update_many(filter, update)
    print(result)

def increase_salary(collection):
    filter={
        "city":{"$nin":["Баку", "Луго","Эльче","Душанбе"]},
        "job":{"$in":["Врач", "Строитель", "Учитель", "Бухгалтер"]},
        "age":{"$gt":18, "$lt":45}
    }
    update={
        "$mul": {
            "salary": 1.1
        }
    }
    result=collection.update_many(filter, update)
    print(result)

def delete_year(collection):
    result=collection.delete_many({
        "year":{"$in":[2005,2006,2007]
                }
        }
    )
    print(result)

filename = "task_3_item.text"
data = get_from_text(filename)
#insert_many(connect(), data)

#delete_salary(connect())
#update_age(connect())
#increase_salary_by_job(connect())
#increase_salary_by_city(connect())
#increase_salary(connect())
#delete_year(connect())

