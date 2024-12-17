from pymongo import MongoClient, DESCENDING, ASCENDING
import json

def read_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        employees = json.load(file)
        
        return(employees)

def connect_db():
    client = MongoClient('localhost', 27017)
    db = client['db']
    
    return db.employees

def first_query(collection):
    results = list(collection                   
                   .aggregate([
                       {'$group': {
                           '_id': "result",
                           'min_salary': {'$min': '$salary'},
                           'avg_salary': {'$avg': '$salary'},
                           'max_salary': {'$max': '$salary'}
                       }}                       
                   ]))
    
    for result in results:
        del result['_id']

    with open('second_task_result_first_query.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

def second_query(collection):
    results = list(collection                   
                   .aggregate([
                       {'$group': {
                           '_id': "$job",
                           'count': {'$sum': 1}                           
                       }}                       
                   ]))

    with open('second_task_result_second_query.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

def third_query(collection):
    results = list(collection                                    
                   .aggregate([
                       {'$group': {
                           '_id': "$city",
                           'min_salary': {'$min': '$salary'},
                           'avg_salary': {'$avg': '$salary'},
                           'max_salary': {'$max': '$salary'}
                       }}                       
                   ]))

    with open('second_task_result_third_query.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

def fourth_query(collection):
    results = list(collection                                    
                   .aggregate([
                       {'$group': {
                           '_id': "$job",
                           'min_salary': {'$min': '$salary'},
                           'avg_salary': {'$avg': '$salary'},
                           'max_salary': {'$max': '$salary'}
                       }}                       
                   ]))

    with open('second_task_result_fourth_query.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

def fifth_query(collection):
    results = list(collection                                    
                   .aggregate([
                       {'$group': {
                           '_id': "$city",
                           'min_age': {'$min': '$age'},
                           'avg_age': {'$avg': '$age'},
                           'max_age': {'$max': '$age'}
                       }}                       
                   ]))

    with open('second_task_result_fifth_query.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

def sixth_query(collection):
    results = list(collection                                    
                   .aggregate([
                       {'$group': {
                           '_id': "$job",
                           'min_age': {'$min': '$age'},
                           'avg_age': {'$avg': '$age'},
                           'max_age': {'$max': '$age'}
                       }}                       
                   ]))

    with open('second_task_result_sixth_query.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

def seventh_query(collection):
    results = list(collection.find(limit=1).sort({'age': ASCENDING, 'salary': DESCENDING}))    

    for result in results:
        del result['_id']

    with open('second_task_result_seventh_query.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

def eighth_query(collection):
    results = list(collection.find(limit=1).sort({'age': DESCENDING, 'salary': ASCENDING}))    

    for result in results:
        del result['_id']

    with open('second_task_result_eighth_query.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

def ninth_query(collection):
    results = list(collection                                    
                   .aggregate([
                       {'$match': {                           
                           'salary': {'$gt': 50_000}
                       }},
                       {'$group': {
                           '_id': "$city",
                           'min_age': {'$min': '$age'},
                           'avg_age': {'$avg': '$age'},
                           'max_age': {'$max': '$age'}
                       }},
                       {'$sort': {
                           'avg_age': DESCENDING
                       }}                       
                   ])
                )

    with open('second_task_result_ninth_query.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

def tenth_query(collection):
    results = list(collection                                    
                   .aggregate([
                       {'$match': {                           
                           'city': {'$in': ['Эльче','Сьюдад-Реаль','Рига','Ереван']},
                           'job': {'$in': ['Врач', 'Архитектор', 'Учитель', 'Психолог']},
                           '$or': [
                               {'age': {'$gt':18, "$lt":25}},
                               {'age': {'$gt':50, "$lt":65}}
                           ]
                       }},
                       {'$group': {
                           '_id': "result",
                           'min_salary': {'$min': '$salary'},
                           'avg_salary': {'$avg': '$salary'},
                           'max_salary': {'$max': '$salary'}
                       }}                       
                   ])
                )

    with open('second_task_result_tenth_query.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

def eleventh_query(collection):
    results = list(collection                                    
                   .aggregate([
                       {'$match': {                           
                           'city': {'$in': ['Эльче','Сьюдад-Реаль','Рига','Ереван']}                                                      
                       }},
                       {'$group': {
                           '_id': "$job",
                           'min_salary': {'$min': '$salary'},
                           'avg_salary': {'$avg': '$salary'},
                           'max_salary': {'$max': '$salary'}
                       }},
                       {'$sort': {
                           'max_salary': DESCENDING
                       }}
                   ])
                )

    with open('second_task_result_eleventh_query.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)


collection = connect_db()
#collection.insert_many(read_file('task_2_item.json'))
first_query(collection)
second_query(collection)
third_query(collection)
fourth_query(collection)
fifth_query(collection)
sixth_query(collection)
seventh_query(collection)
eighth_query(collection)
ninth_query(collection)
tenth_query(collection)
eleventh_query(collection)