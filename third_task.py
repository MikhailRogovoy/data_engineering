from pymongo import MongoClient, DESCENDING, ASCENDING
import json

def read_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        data = file.read().split("\n=====\n")
        data.remove('')
        employees = []        

        for item in data:
            employee = {}
            properties = item.split('\n')

            for property in properties:
                key_value = property.split('::')
                if (key_value[0] == 'job' or key_value[0] == 'city'): employee[f'{key_value[0]}'] = f'{key_value[1]}'
                else: employee[f'{key_value[0]}'] = int(f'{key_value[1]}')

            employees.append(employee)
        
        return(employees)
    
def connect_db():
    client = MongoClient('localhost', 27017)
    db = client['db']
    
    return db.employees

def delete_by_salary(collection):
    collection.delete_many({
                            '$or': [
                                {'salary': {'$lt': 25_000}},
                                {'salary': {'$gt': 175_000}}
                            ]
                            })
    results = []
    min_salary_after_del = list(collection.find(limit=1).sort({'salary': ASCENDING}))
    max_salary_after_del = list(collection.find(limit=1).sort({'salary': DESCENDING}))    
    results.append(min_salary_after_del[0])
    results.append(max_salary_after_del[0])
    results[0]['_id'] = 'min_salary_in_table_after_del'
    results[1]['_id'] = 'max_salary_in_table_after_del'
    
    with open('third_task_result_delete_by_salary.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

def increase_age(collection):

    results = [] 
    min_age_before_upd = list(collection.find(limit=1).sort({'age': ASCENDING}))
    max_age_before_upd = list(collection.find(limit=1).sort({'age': DESCENDING}))
    results.append(min_age_before_upd[0])
    results.append(max_age_before_upd[0])
    results[0]['_id'] = 'min_age_before_upd_in_table'
    results[1]['_id'] = 'max_age_before_upd_in_table'

    collection.update_many({}, {'$inc': {'age': 1}})
    
    min_age_after_upd = list(collection.find(limit=1).sort({'age': ASCENDING}))
    max_age_after_upd = list(collection.find(limit=1).sort({'age': DESCENDING}))    
    results.append(min_age_after_upd[0])
    results.append(max_age_after_upd[0])
    results[2]['_id'] = 'min_age_after_upd_in_table'
    results[3]['_id'] = 'max_age_after_upd_in_table'
    
    with open('third_task_result_increase_age.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

def increase_salary_by_job(collection):

    results = [] 
    min_age_before_upd = list(collection
                              .find({'job': {'$in': ['Учитель','Врач','Инженер']}},limit=1)
                              .sort({'salary': ASCENDING}))
    max_age_before_upd = list(collection
                              .find({'job': {'$in': ['Учитель','Врач','Инженер']}}, limit=1)
                              .sort({'salary': DESCENDING}))
    results.append(min_age_before_upd[0])
    results.append(max_age_before_upd[0])
    results[0]['_id'] = 'min_salary_by_job_before_upd_in_table'
    results[1]['_id'] = 'max_salary_by_job_before_upd_in_table'

    collection.update_many({'job': {'$in': ['Учитель','Врач','Инженер']}}, {'$mul': {'salary': 1.05}})
    
    min_age_after_upd = list(collection
                              .find({'job': {'$in': ['Учитель','Врач','Инженер']}},limit=1)
                              .sort({'salary': ASCENDING}))
    max_age_after_upd = list(collection
                              .find({'job': {'$in': ['Учитель','Врач','Инженер']}}, limit=1)
                              .sort({'salary': DESCENDING}))
    results.append(min_age_after_upd[0])
    results.append(max_age_after_upd[0])
    results[2]['_id'] = 'min_salary_by_job_after_upd_in_table'
    results[3]['_id'] = 'max_salary_by_job_after_upd_in_table'
    
    with open('third_task_result_increase_salary_by_job.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

def increase_salary_by_city(collection):

    results = [] 
    min_age_before_upd = list(collection
                              .find({'city': {'$in': ['Барселона','Санкт-Петербург','Будапешт']}},limit=1)
                              .sort({'salary': ASCENDING}))
    max_age_before_upd = list(collection
                              .find({'city': {'$in': ['Барселона','Санкт-Петербург','Будапешт']}}, limit=1)
                              .sort({'salary': DESCENDING}))
    results.append(min_age_before_upd[0])
    results.append(max_age_before_upd[0])
    results[0]['_id'] = 'min_salary_by_city_before_upd_in_table'
    results[1]['_id'] = 'max_salary_by_city_before_upd_in_table'

    collection.update_many({'city': {'$in': ['Барселона','Санкт-Петербург','Будапешт']}}, {'$mul': {'salary': 1.07}})
    
    min_age_after_upd = list(collection
                              .find({'city': {'$in': ['Барселона','Санкт-Петербург','Будапешт']}},limit=1)
                              .sort({'salary': ASCENDING}))
    max_age_after_upd = list(collection
                              .find({'city': {'$in': ['Барселона','Санкт-Петербург','Будапешт']}}, limit=1)
                              .sort({'salary': DESCENDING}))
    results.append(min_age_after_upd[0])
    results.append(max_age_after_upd[0])
    results[2]['_id'] = 'min_salary_by_city_after_upd_in_table'
    results[3]['_id'] = 'max_salary_by_city_after_upd_in_table'
    
    with open('third_task_result_increase_salary_by_city.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

def increase_salary_by_complex_cond(collection, city, jobs, gt_age, lt_age):

    results = [] 
    min_age_before_upd = list(collection
                              .find({'city': city,
                                    'job': {'$in': jobs},
                                    'age': {'$gt': gt_age, '$lt': lt_age}},
                                    limit=1)
                              .sort({'salary': ASCENDING}))
    max_age_before_upd = list(collection
                              .find({'city': city,
                                    'job': {'$in': jobs},
                                    'age': {'$gt': gt_age, '$lt': lt_age}},
                                    limit=1)
                              .sort({'salary': DESCENDING}))
    
    results.append(min_age_before_upd[0])
    results.append(max_age_before_upd[0])
    results[0]['_id'] = 'min_salary_by_complex_cond_before_upd_in_table'
    results[1]['_id'] = 'max_salary_by_complex_cond_before_upd_in_table'

    collection.update_many({'city': city,
                            'job': {'$in': jobs},
                            'age': {'$gt': gt_age, '$lt': lt_age}}, 
                            {'$mul': {'salary': 1.10}})
    
    min_age_after_upd = list(collection
                              .find({'city': city,
                                    'job': {'$in': jobs},
                                    'age': {'$gt': gt_age, '$lt': lt_age}},
                                    limit=1)
                              .sort({'salary': ASCENDING}))
    max_age_after_upd = list(collection
                              .find({'city': city,
                                    'job': {'$in': jobs},
                                    'age': {'$gt': gt_age, '$lt': lt_age}},
                                    limit=1)
                              .sort({'salary': DESCENDING}))
    
    results.append(min_age_after_upd[0])
    results.append(max_age_after_upd[0])
    results[2]['_id'] = 'min_salary_by_complex_cond_after_upd_in_table'
    results[3]['_id'] = 'max_salary_by_complex_cond_after_upd_in_table'
    
    with open('third_task_result_increase_salary_by_complex_cond.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

def delete_by_complex_cond(collection):

    results = []
    min_age_before_del = list(collection.find(limit=1).sort({'age': ASCENDING}))
    results.append(min_age_before_del[0])
    results[0]['_id'] = 'min_age_in_table_before_del'

    collection.delete_many({
                            '$and': [
                                {'age': {'$lt': 25}},
                                {'age': {'$gt': 18}}
                            ]
                            })
    
    min_age_after_del = list(collection.find(limit=1).sort({'age': ASCENDING}))        
    results.append(min_age_after_del[0])  
    results[1]['_id'] = 'third_task_min_age_in_table_after_del'
    
    with open('third_task_result_delete_by_complex_cond.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

collection = connect_db()
#collection.insert_many(read_file('task_3_item.text'))
#delete_by_salary(collection)
#increase_age(collection)
#increase_salary_by_job(collection)
#increase_salary_by_city(collection)
#increase_salary_by_complex_cond(collection, 'Хихон', ['Медсестра', 'Врач', 'IT-специалист'], 25, 60)
#delete_by_complex_cond(collection)