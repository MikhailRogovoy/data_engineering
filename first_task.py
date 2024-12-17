from pymongo import MongoClient, DESCENDING, ASCENDING
import pickle, json

def read_file(filepath):
    with open(filepath, 'rb') as file:
        employees = pickle.load(file)
        
        return(employees)

def connect_db():
    client = MongoClient('localhost', 27017)
    db = client['db']
    
    return db.employees

def get_sort_by_salary(collection):
    results = list(collection.find(limit=10).sort({'salary': DESCENDING}))
    
    for result in results:
        del result['_id']

    with open('first_task_result_sort_by_salary.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

def get_filter_by_age(collection):
    results = list(collection
                   .find({'age': {'$lt': 30}}, limit=15)
                   .sort({'salary': DESCENDING}))
    
    for result in results:
        del result['_id']

    with open('first_task_result_filter_by_age.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

def get_complex_filter(collection):
    results = list(collection
                   .find({'city': 'Пласенсия',
                          'job': {'$in': ['Водитель', 'Продавец', 'Учитель']}
                          }, limit=10)
                   .sort({'age': ASCENDING}))
    
    for result in results:
        del result['_id']

    with open('first_task_result_complex_filter.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

def get_records_count(collection):
    result = collection.count_documents({
                                        'age': {'$gt': 25, '$lt': 35},
                                        'year': {'$gte': 2019, '$lte': 2022},
                                        '$or': [
                                            {'salary': {'$gt': 50_000, '$lte': 75_000}},
                                            {'salary': {'$gt': 125_000, '$lt': 150_000}}
                                            ]
                                        })

    count_result = {'records_count': result}

    with open('first_task_result_records_count.json', 'w', encoding='utf-8') as f:
        json.dump(count_result, f, ensure_ascii=False, indent=4)

collection = connect_db()
#collection.insert_many(read_file('task_1_item.pkl'))
get_sort_by_salary(collection)
get_filter_by_age(collection)
get_complex_filter(collection)
get_records_count(collection)