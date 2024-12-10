import csv
import msgpack
import sqlite3
import json

def read_msgpack(filepath):
    with open(filepath, 'rb') as file:
        data_msgpack = msgpack.load(file)
        for item in data_msgpack:
            item['duration_ms'] = int(item['duration_ms'])
            item['year'] = int(item['year'])
            item['tempo'] = float(item['tempo'])
            item['mode'] = int(item['mode'])
            item['speechiness'] = float(item['speechiness'])
            item['acousticness'] = float(item['acousticness'])
            item['instrumentalness'] = float(item['instrumentalness'])
    return data_msgpack

def read_csv(filepath):
    with open(filepath, 'r', newline='', encoding='utf-8') as file:
        data_csv = list(csv.DictReader(file, delimiter=';'))
        for item in data_csv:
            item['duration_ms'] = int(item['duration_ms'])
            item['year'] = int(item['year'])
            item['tempo'] = float(item['tempo'])
            item['energy'] = float(item['energy'])
            item['key'] = int(item['key'])
            item['loudness'] = float(item['loudness'])

    return data_csv

def connect_to_db(dbname):
    db = sqlite3.connect(dbname)
    db.row_factory = sqlite3.Row
    return db

def create_songs_table():
    db = connect_to_db('third_task.db')
    cur = db.cursor()
    cur.execute("""
            CREATE TABLE songs (
                id integer primary key,
                artist text,
                song text,
                duration_ms integer,
                year text,
                tempo float,
                genre text)
                """)

def insert_data(db, data):
    cur = db.cursor()
    cur.executemany("""
                INSERT INTO songs (artist, song, duration_ms, year, tempo, genre)
                VALUES (:artist, :song, :duration_ms, :year, :tempo, :genre)
                    """, data)
    db.commit()

def first_query(db):
    cur = db.cursor()
    result = cur.execute("""
                SELECT *
                FROM songs
                ORDER BY year
                LIMIT 30
                """)

    songs = []
    for row in result.fetchall():
        songs.append(dict(row))

    filename = 'third_task_sort_res.json'
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(songs, file, ensure_ascii=False, indent=4)

def second_query(db):
    cur = db.cursor()
    result = cur.execute("""
                SELECT
                    COUNT(*) as songs_count, 
                    MIN(duration_ms) as min_duration_ms_of_song,
                    MAX(duration_ms) as max_duration_ms_of_song,
                    ROUND(AVG(duration_ms), 2) as avg_duration_ms_of_song
                FROM songs              
                """)

    num_field_output = {}
    for row in result.fetchall():
        num_field_output = dict(row)

    filename = 'third_task_num_res.json'
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(num_field_output, file, ensure_ascii=False, indent=4)

def third_query(db):
    cur = db.cursor()
    result = cur.execute("""
                SELECT
                    COUNT(*) as count,
                    artist                                  
                FROM songs
                GROUP BY artist   
                """)

    categ_field_output = []
    for row in result.fetchall():
        categ_field_output.append(dict(row))
       

    filename = 'third_task_categ_res.json'
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(categ_field_output, file, ensure_ascii=False, indent=4)

def fourth_query(db):
    cur = db.cursor()
    result = cur.execute("""
                SELECT *                    
                FROM songs
                WHERE year > 2010
                ORDER BY duration_ms DESC
                LIMIT 30
                """)

    sort_predic_output = []
    for row in result.fetchall():
        sort_predic_output.append(dict(row))
       

    filename = 'third_task_sort_predic_res.json'
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(sort_predic_output, file, ensure_ascii=False, indent=4)

# Step 1:
#create_songs_table()
# 
# Step 2: 
db = connect_to_db('third_task.db')
#insert_data(db=db, data=read_msgpack('_part_1.msgpack'))
#insert_data(db=db, data=read_csv('_part_2.csv'))
#
# Step 3: 
first_query(db)
second_query(db)
third_query(db)
fourth_query(db)
