import sqlite3
import msgpack
import json

def read_msgpack(filename):
    with open(filename, 'rb') as file:
        subitem = msgpack.load(file)        
    return subitem

def connect_to_db(dbname):
    db = sqlite3.connect(dbname)
    db.row_factory = sqlite3.Row
    return db

def create_prise_table():
    db = connect_to_db('first_task.db')
    cur = db.cursor()
    cur.execute("""
            CREATE TABLE prise (
                id integer primary key,
                name text references tournament(name),
                place integer,
                prise integer
                )
                """)
    
def insert_data(db, data):
    cur = db.cursor()
    cur.executemany("""
                INSERT INTO prise (name, place, prise)
                VALUES (:name, :place, :prise)
                    """, data)
    db.commit()

def first_query(db):
    cur = db.cursor()
    result = cur.execute("""
                SELECT *
                FROM prise
                WHERE name = 'Европа 1975'
                ORDER BY place                
                """)

    ord_place_result = []
    for row in result.fetchall():
        ord_place_result.append(dict(row))

    filename = 'second_task_ord_place_res.json'
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(ord_place_result, file, ensure_ascii=False, indent=4)

def second_query(db):
    cur = db.cursor()
    result = cur.execute("""
                SELECT t.name, t.id, p.prise, p.place
                FROM tournament t
                JOIN prise p ON t.name = p.name
                WHERE p.place = 2                               
                """)

    join_name_prise_result = []
    for row in result.fetchall():
        join_name_prise_result.append(dict(row))

    filename = 'second_task_join_name_prise_res.json'
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(join_name_prise_result, file, ensure_ascii=False, indent=4)

def third_query(db):
    cur = db.cursor()
    result = cur.execute("""
                SELECT t.name, t.city, p.prise, p.place
                FROM tournament t
                JOIN prise p ON t.name = p.name
                WHERE p.prise < 100000
                GROUP BY p.prise          
                """)

    join_name_prise_result = []
    for row in result.fetchall():
        join_name_prise_result.append(dict(row))

    filename = 'second_task_prise_cond_res.json'
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(join_name_prise_result, file, ensure_ascii=False, indent=4)

# Step 1:
create_prise_table()

# Step 2:
data = read_msgpack('subitem.msgpack')
db = connect_to_db('first_task.db')
insert_data(db=db, data=data)

# Step 3:
first_query(db)
second_query(db)
third_query(db)