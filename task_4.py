from bs4 import BeautifulSoup
import json
import pandas as pd
import numpy as np

items = []

def handle_file():
    for filename in range (1, 207):
        with open(f'{filename}.xml', 'r', encoding='utf-8') as file:
            xml_content = file.read()
        
        soup = BeautifulSoup(xml_content, features='xml')
        products = soup.find_all(name='clothing')  

        for product in products:
            item = {}

            item['id'] = int(product.find('id').get_text(strip=True))
            item['name'] = product.find('name').get_text(strip=True)
            item['category'] = product.find('category').get_text(strip=True)
            item['size'] = product.find('size').get_text(strip=True)        
            item['color'] = product.find('color').get_text(strip=True) 
            item['material'] = product.find('material').get_text(strip=True)
            item['price'] = int(product.find('price').get_text(strip=True))
            item['rating'] = float(product.find('rating').get_text(strip=True))
            item['reviews'] = int(product.find('reviews').get_text(strip=True))

            other_tags = product.find_all(['new', 'exclusive', 'sporty'])        
            for tag in other_tags:
                item[f'{tag.name}'] = tag.get_text(strip=True)

            items.append(item)  

    with open('task_4_result.json', 'w', encoding='utf-8') as file:
        json.dump(items, file, ensure_ascii=False, indent = 4)

data = pd.read_json('task_4_result.json')

def get_sorted(data):
    sorted_data = data.sort_values(by=['price'], ignore_index=True)    
    sorted_data = sorted_data.to_dict(orient='index')
    sorted_products_by_price = list(sorted_data.values())
    
    for product in sorted_products_by_price:        
        if (str(product['new']) == 'nan'): product.pop('new')            
        if (str(product['exclusive']) == 'nan'): product.pop('exclusive')
        if (str(product['sporty']) == 'nan'): product.pop('sporty')
    
    with open('task_4_sorted_products_by_price.json', 'w', encoding='utf-8') as file:
        json.dump(sorted_products_by_price, file, ensure_ascii=False, indent = 4)

def get_filtered(data):
    filtered_data = data.copy()    
    filtered_data.drop(filtered_data[filtered_data.rating < 4.0].index, inplace = True)
    filtered_data.reset_index(drop=True ,inplace = True)    
    filtered_data = filtered_data.to_dict(orient='index')
    filtered_books_by_rating = list(filtered_data.values())

    for product in filtered_books_by_rating:        
        if (str(product['new']) == 'nan'): product.pop('new')            
        if (str(product['exclusive']) == 'nan'): product.pop('exclusive')
        if (str(product['sporty']) == 'nan'): product.pop('sporty')

    with open('task_4_filtered_products_by_rating.json', 'w', encoding='utf-8') as file:
        json.dump(filtered_books_by_rating, file, ensure_ascii=False, indent = 4)

charact = []

def get_numeric_charact(data):
    numeric_charact = {}
                    
    numeric_charact[f'sum_rating'] = data['rating'].sum()
    numeric_charact[f'max_rating'] = data['rating'].max()
    numeric_charact[f'min_rating'] = data['rating'].min()
    numeric_charact[f'mean_rating'] = data['rating'].mean()
    numeric_charact[f'std_rating'] = data['rating'].std()

    for key in numeric_charact.keys():
        if (type(numeric_charact[key]) == np.int64):
            numeric_charact[key] = int(numeric_charact[key])
        else:
            numeric_charact[key] = float(numeric_charact[key])

    charact.append(numeric_charact)

def get_categorial_charact(data):
    categorial_charact = {}
    
    for word in data['material']:
        if (categorial_charact.get(word) == None):
            categorial_charact[word] = 1
        else:
            categorial_charact[word] = categorial_charact[word] + 1
        
    charact.append(categorial_charact)

def get_result_in_json():
    with open('task_4_charact_result.json', 'w', encoding='utf-8') as file:
        json.dump(charact, file, ensure_ascii=False, indent = 4)

handle_file()
get_sorted(data=data)
get_filtered(data=data)
get_numeric_charact(data=data)
get_categorial_charact(data)
get_result_in_json()