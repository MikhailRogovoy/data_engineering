import pickle
import sqlite3
import json

def read_file(filepath):
    with open(filepath, 'rb') as file:
        items = pickle.load(file)
    
    return items

def connect_to_db(dbname):
    db = sqlite3.connect(dbname)
    db.row_factory = sqlite3.Row
    return db

def create_tournament_table():
    db = connect_to_db('first_task.db')
    cur = db.cursor()
    cur.execute("""
            CREATE TABLE tournament (
                id integer primary key,
                name text,
                city text,
                begin text,
                system text,
                tours_count integer,
                min_rating integer,
                time_on_game integer
                )
                """)

def insert_data(db, data):
    cur = db.cursor()
    cur.executemany("""
                INSERT INTO tournament (id, name, city, begin, system, tours_count, min_rating, time_on_game)
                VALUES (:id, :name, :city, :begin, :system, :tours_count, :min_rating, :time_on_game)
                    """, data)
    db.commit()
    
def first_query(db):
    cur = db.cursor()
    result = cur.execute("""
                SELECT *
                FROM tournament
                ORDER BY time_on_game
                LIMIT 30
                """)

    items = []
    for row in result.fetchall():
        items.append(dict(row))

    filename = 'first_task_sort_res.json'
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(items, file, ensure_ascii=False, indent=4)

def second_query(db):
    cur = db.cursor()
    result = cur.execute("""
                SELECT
                    COUNT(*) as tournament_count, 
                    MIN(time_on_game) as min_time_on_game,
                    MAX(time_on_game) as max_time_on_game,
                    ROUND(AVG(min_rating), 2) as avg_min_rating
                FROM tournament               
                """)

    num_field_output = {}
    for row in result.fetchall():
        num_field_output = dict(row)

    filename = 'first_task_num_res.json'
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(num_field_output, file, ensure_ascii=False, indent=4)

def third_query(db):
    cur = db.cursor()
    result = cur.execute("""
                SELECT
                    COUNT(*) as count,
                    city                                  
                FROM tournament
                GROUP BY city   
                """)

    categ_field_output = []
    for row in result.fetchall():
        categ_field_output.append(dict(row))
       

    filename = 'first_task_categ_res.json'
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(categ_field_output, file, ensure_ascii=False, indent=4)

def fourth_query(db):
    cur = db.cursor()
    result = cur.execute("""
                SELECT *                    
                FROM tournament
                WHERE min_rating < 2600
                ORDER BY min_rating DESC
                LIMIT 30
                """)

    sort_predic_output = []
    for row in result.fetchall():
        sort_predic_output.append(dict(row))
       

    filename = 'first_task_sort_predic_res.json'
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(sort_predic_output, file, ensure_ascii=False, indent=4)

# Step 1:
create_tournament_table()
# 
# Step 2: 
data = read_file('item.pkl')
db = connect_to_db('first_task.db')
insert_data(db=db, data=data)
#
# Step 3: 
first_query(db)
second_query(db)
third_query(db)
fourth_query(db)