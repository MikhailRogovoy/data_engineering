import csv
import msgpack
import sqlite3
import json

def read_csv(filepath):
    with open(filepath, 'r', newline='', encoding='utf-8') as file:
        data_csv = list(csv.DictReader(file, delimiter=';'))
        products = []
        for item in data_csv:
            product = {}
            if item['views'] is None: continue
            else:
                product['name'] = item['name']
                product['price'] = float(item['price'])
                product['quantity'] = int(item['quantity'])
                product['category'] = item['category']
                product['fromCity'] = item['fromCity']
                product['isAvailable'] = 1 if item['isAvailable'] == "True" else 0
                product['views'] = int(item['views'])
                products.append(product)

    return products

def read_msgpack(filepath):
    with open(filepath, 'rb') as file:
        data_msgpack = msgpack.load(file)        

    return data_msgpack

def connect_to_db(dbname):
    db = sqlite3.connect(dbname)
    db.row_factory = sqlite3.Row
    return db

def create_products_table():
    db = connect_to_db('fourth_task_res.db')
    cur = db.cursor()
    cur.execute("""
            CREATE TABLE products (
                id integer primary key,
                name text,
                price float,
                quantity integer,
                category text,
                fromCity text,
                isAvailable integer,
                views integer,
                version integer default 0)
                """)

def insert_data(db, data):
    cur = db.cursor()
    cur.executemany("""
                INSERT INTO products (name, price, quantity, category, fromCity, isAvailable, views)
                VALUES (:name, :price, :quantity, :category, :fromCity, :isAvailable, :views)
                    """, data)
    db.commit()

def update_price_abs(db, update):       
    cur = db.cursor()
    cur.execute("BEGIN")
    cur.execute("""
                UPDATE products                   
                SET price = ROUND(price + ?, 2),
                    version = version + 1
                WHERE name = ?
                """, (update['param'], update['name']))
    result = cur.execute("""
                        SELECT * FROM products WHERE price < 0                             
                        """)
    results = []
    for row in result.fetchall():
        results.append(dict(row))    
    if (len(results) == 0): db.commit()
    else: db.rollback()

def update_available(db, update):
    cur = db.cursor()
    cur.execute("""            
            UPDATE products                   
            SET isAvailable = ?,
                version = version + 1
            WHERE name = ?                  
            """, (update['param'], update['name']))
    db.commit()

def update_remove(db, name):
    cur = db.cursor()    
    cur.execute("""
            DELETE from products                
            WHERE name = ?                  
            """, (name,))
    db.commit()

def update_quantity_add(db, update):
    cur = db.cursor()    
    cur.execute("""            
            UPDATE products                   
            SET quantity = quantity + ?,
                version = version + 1
            WHERE name = ?;                                  
            """, (update['param'], update['name']))
    db.commit()

def update_price_percent(db, update):
    cur = db.cursor()
    cur.execute("""            
            UPDATE products                   
            SET price = ROUND(price * (1 + ?), 2),
                version = version + 1
            WHERE name = ?;            
            """, (update['param'], update['name']))
    db.commit()

def update_quantity_sub(db, update):
    cur = db.cursor()
    cur.execute("BEGIN")
    cur.execute("""            
            UPDATE products                   
            SET quantity = quantity - ?,
                version = version + 1
            WHERE name = ?;            
            """, (update['param'], update['name']))
    result = cur.execute("""
                        SELECT * FROM products WHERE quantity < 0                             
                        """)
    results = []
    for row in result.fetchall():
        results.append(dict(row))    
    if (len(results) == 0): db.commit()
    else: db.rollback() 

def handle_updates(db, updates):
    removed_products = []    
    for update in updates:
        if (update['method'] == 'remove' and removed_products.count(update['name']) == 0):
            removed_products.append(update['name'])
            update_remove(db, update['name'])
        if update['method'] == 'price_abs': update_price_abs(db, update)
        if update['method'] == 'available': update_available(db, update)        
        if update['method'] == 'quantity_add': update_quantity_add(db, update)
        if update['method'] == 'price_percent': update_price_percent(db, update)
        if update['method'] == 'quantity_sub': update_quantity_sub(db, update)

def first_query(db):
    cur = db.cursor()
    result = cur.execute("""
                SELECT *
                FROM products
                ORDER BY version DESC
                LIMIT 10
                """)

    products = []
    for row in result.fetchall():
        products.append(dict(row))

    filename = 'fourth_task_first_query.json'
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(products, file, ensure_ascii=False, indent=4)

def second_query(db):
    cur = db.cursor()
    result = cur.execute("""
                SELECT
                    category as category_product,
                    COUNT(*) as category_product_count,
                    SUM(price) as sum_price_category_product, 
                    MIN(price) as min_price_category_product,
                    MAX(price) as max_price_category_product,
                    ROUND(AVG(price), 2) as avg_price_category_product
                FROM products
                GROUP BY category             
                """)

    products = []
    for row in result.fetchall():
        products.append(dict(row))

    filename = 'fourth_task_second_query.json'
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(products, file, ensure_ascii=False, indent=4)

def third_query(db):
    cur = db.cursor()
    result = cur.execute("""
                SELECT
                    category as category_product,
                    COUNT(*) as category_product_count,
                    SUM(quantity) as sum_quantity_category_product, 
                    MIN(quantity) as min_quantity_category_product,
                    MAX(quantity) as max_quantity_category_product,
                    ROUND(AVG(quantity), 2) as avg_quantity_category_product
                FROM products
                GROUP BY category             
                """)

    products = []
    for row in result.fetchall():
        products.append(dict(row))

    filename = 'fourth_task_third_query.json'
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(products, file, ensure_ascii=False, indent=4)

def fourth_query(db):
    cur = db.cursor()
    result = cur.execute("""
                SELECT *
                FROM products
                ORDER BY views DESC
                LIMIT 30                          
                """)

    products = []
    for row in result.fetchall():
        products.append(dict(row))

    filename = 'fourth_task_fourth_query.json'
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(products, file, ensure_ascii=False, indent=4)

# Step 1:
create_products_table()
# 
# Step 2: 
db = connect_to_db('fourth_task_res.db')
insert_data(db=db, data=read_csv('_product_data.csv'))
# 
# Step 3: 
handle_updates(db=db, updates=read_msgpack('_update_data.msgpack'))
# 
# Step 4:
first_query(db)
second_query(db)
third_query(db)
fourth_query(db)
