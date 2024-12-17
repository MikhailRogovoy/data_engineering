import csv
import json
import sqlite3

def read_csv_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        data_csv = list(csv.DictReader(file, delimiter=','))

        car_data = []
        for item in data_csv:
            car_info = {}
            car_info['car_id'] = item['car_id']            
            car_info['Car_Name'] = item['Car_Name']
            car_info['Year'] = int(item['Year'])
            car_info['Selling_Price'] = float(item['Selling_Price'])
            car_info['Present_Price'] = float(item['Present_Price'])
            car_info['Kms_Driven'] = int(item['Kms_Driven'])            
            car_data.append(car_info)    

    return car_data

def read_json_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        car_data_addit = json.load(file)        
    return car_data_addit


def connect_to_db(dbname):
    db = sqlite3.connect(dbname)
    db.row_factory = sqlite3.Row
    return db

def create_cars_info_tables(dbname):
    db = connect_to_db(dbname)
    cur = db.cursor()
    cur.execute("""
            CREATE TABLE cars_common_info (
                car_id integer primary key,
                Car_Name text,
                Year integer,
                Present_Price float)
                """)
    
    cur.execute("""
            CREATE TABLE cars_current_info (
                car_id integer primary key,
                Car_Name text,                
                Kms_Driven integer,
                Selling_Price float)
                """)
    
    cur.execute("""
            CREATE TABLE cars_sales_info (
                car_id integer primary key,
                Car_Name text,
                Owner integer,                
                Seller_Type text)
                """)

    cur.execute("""
            CREATE TABLE cars_properties_info (
                car_id integer primary key,
                Car_Name text,
                Fuel_Type text,
                Transmission text)
                """)

def insert_data(db, common_info, properties_info):

    current_info = common_info
    sales_info = properties_info    

    cur = db.cursor()
    cur.executemany("""
                INSERT INTO cars_common_info (car_id, Car_Name, Year, Present_Price)
                VALUES (:car_id, :Car_Name, :Year, :Present_Price)
                    """, common_info)
    cur.executemany("""
                INSERT INTO cars_current_info (car_id, Car_Name, Kms_Driven, Selling_Price)
                VALUES (:car_id, :Car_Name, :Kms_Driven, :Selling_Price)
                    """, current_info)
    
    cur.executemany("""
                INSERT INTO cars_sales_info (car_id, Car_Name, Owner, Seller_Type)
                VALUES (:car_id, :Car_Name, :Owner, :Seller_Type)
                    """, sales_info)

    cur.executemany("""
                INSERT INTO cars_properties_info (car_id, Car_Name, Fuel_Type, Transmission)
                VALUES (:car_id, :Car_Name, :Fuel_Type, :Transmission)
                    """, properties_info)
    
    db.commit()

def get_more_common_info(db):
    cur = db.cursor()
    result = cur.execute("""
                SELECT cci.car_id, cci.Car_name, cci.Year, cpi.Fuel_type, cpi.Transmission
                FROM cars_common_info cci
                JOIN cars_properties_info cpi ON cci.car_id = cpi.car_id
                WHERE cci.Present_Price > 8                               
                """)

    more_common_info_result = []
    for row in result.fetchall():
        more_common_info_result.append(dict(row))

    filename = 'fifth_task_more_common_info_res.json'
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(more_common_info_result, file, ensure_ascii=False, indent=4)

def get_min_cars_price(db):
    cur = db.cursor()
    result = cur.execute("""
                SELECT
                    cci.Car_Name as Car_name,                    
                    MIN(Selling_Price) as min_selling_price                    
                FROM cars_current_info cci
                GROUP BY cci.Car_Name               
                """)

    min_cars_price_result = []
    for row in result.fetchall():
        min_cars_price_result.append(dict(row))

    filename = 'fifth_task_min_cars_price_res.json'
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(min_cars_price_result, file, ensure_ascii=False, indent=4)

def get_min_cars_driven_automatic(db):
    cur = db.cursor()
    result = cur.execute("""
                SELECT
                    cci.Car_Name,                                        
                    MIN(Kms_Driven) as min_Kms_Driven,
                    cpi.Transmission                    
                FROM cars_current_info cci
                JOIN cars_properties_info cpi ON cci.car_id = cpi.car_id
                WHERE cpi.Transmission = 'Automatic'
                GROUP BY cci.Car_Name               
                """)

    min_cars_driven_automatic_result = []
    for row in result.fetchall():
        min_cars_driven_automatic_result.append(dict(row))

    filename = 'fifth_min_cars_driven_automatic_res.json'
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(min_cars_driven_automatic_result, file, ensure_ascii=False, indent=4)

def get_max_cars_year(db):
    cur = db.cursor()
    result = cur.execute("""
                SELECT
                    cci.Car_Name,
                    MAX(Year) as max_year
                FROM cars_common_info cci
                WHERE cci.Year BETWEEN 2015 AND 2017
                GROUP BY cci.Car_Name
                """)

    max_cars_year_result = []
    for row in result.fetchall():
        max_cars_year_result.append(dict(row))

    filename = 'fifth_max_cars_year_res.json'
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(max_cars_year_result, file, ensure_ascii=False, indent=4)

def get_cars_seller_min_price(db):
    cur = db.cursor()
    result = cur.execute("""
                SELECT
                    csi.Car_Name,                                        
                    MIN(cci.Selling_Price) as min_selling_price,
                    csi.Seller_type as seller                   
                FROM cars_sales_info csi                
                JOIN cars_current_info cci ON csi.car_id = cci.car_id
                WHERE csi.Seller_type = "Individual"
                GROUP BY csi.Car_Name              
                """)

    max_cars_seller_min_price_result = []
    for row in result.fetchall():
        max_cars_seller_min_price_result.append(dict(row))

    filename = 'fifth_cars_seller_min_price_res.json'
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(max_cars_seller_min_price_result, file, ensure_ascii=False, indent=4)

def cars_petrol_count(db):
    cur = db.cursor()
    result = cur.execute("""
                SELECT
                    COUNT(*) as cars_count,
                    cpi.Fuel_Type as fuel_type
                FROM cars_properties_info cpi
                WHERE cpi.Fuel_Type = "Petrol"              
                """)

    count_cars_petrol = {}
    for row in result.fetchall():
        count_cars_petrol = dict(row)

    filename = 'fifth_count_cars_petrol_res.json'
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(count_cars_petrol, file, ensure_ascii=False, indent=4)



# Step 1: Create database
#create_cars_info_tables('fifth_task_res.db')
 
# Step 2: Insert data
db = connect_to_db('fifth_task_res.db')
#insert_data(db=db, common_info=read_csv_file('fifth_task_car_data.csv'), properties_info=read_json_file('fifth_task_car_data_addit.json'))

# Step 3: Make requests:
get_more_common_info(db) #Добавляем данные к году выпуска: тип топлива и тип трансмиссии для каждого автомобиля
get_min_cars_price(db) #Находим минимальную цену для каждой марки автомобиля
get_min_cars_driven_automatic(db) #Находим данные по минимальному пробегу и автоматической коробке
get_max_cars_year(db) #Находим данные по "самым молодым" автомобилям в таблице для каждой марки автомобилей 
get_cars_seller_min_price(db) #Находим данные продаввцу и минимальной цене по каждой группе автомобилей
cars_petrol_count(db) #Находим количество автомобилей в таблице с бензиновым двигателем