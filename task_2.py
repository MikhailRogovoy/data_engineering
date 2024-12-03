from bs4 import BeautifulSoup
import json
import pandas as pd
import numpy as np

items = []

def handle_file():
    for filename in range (1, 50):
        with open(f'{filename}.html', 'r', encoding='utf-8') as file:
            html_content = file.read()
        
        soup = BeautifulSoup(html_content, features='html.parser')
        products = soup.find_all(name='div', attrs={'class': 'pad'})

        for product in products:
            item = {}  

            item['id'] = int(product.a['data-id'])
            item['link'] = product.find_all('a')[1]['href']
            item['img'] = product.img['src']
            item['model'] = product.find_all('span')[0].get_text(strip=True)        
            item['price'] = int(product.find_all('price')[0].get_text(strip=True).replace(' ', '').replace('₽', ''))
            item['bonus'] = int(product.find_all('strong')[0].get_text(strip=True).strip().split(' ')[2])
            
            li_tags = product.find_all('li')        
            for tag in li_tags:           
                item[f'{list(tag.attrs.values())[0]}'] = tag.get_text(strip=True)

            items.append(item)  

    with open('task_2_result.json', 'w', encoding='utf-8') as file:
        json.dump(items, file, ensure_ascii=False, indent = 4)

data = pd.read_json('task_2_result.json')

def get_sorted(data):
    sorted_data = data.sort_values(by=['price'], ignore_index=True)    
    sorted_data = sorted_data.to_dict(orient='index')
    sorted_products_by_price = list(sorted_data.values())

    for product in sorted_products_by_price:        
        if (str(product['processor']) == 'nan'): product.pop('processor')            
        if (str(product['sim']) == 'nan'): product.pop('sim')
        if (str(product['camera']) == 'nan'): product.pop('camera')
        if (str(product['acc']) == 'nan'): product.pop('acc')
        if (str(product['matrix']) == 'nan'): product.pop('matrix')
        if (str(product['ram']) == 'nan'): product.pop('ram')
        if (str(product['resolution']) == 'nan'): product.pop('resolution')       
    
    with open('task_2_sorted_products_by_price.json', 'w', encoding='utf-8') as file:
        json.dump(sorted_products_by_price, file, ensure_ascii=False, indent = 4)

def get_filtered(data):
    filtered_data = data.copy()    
    filtered_data.drop(filtered_data[filtered_data.bonus < 4000].index, inplace = True)
    filtered_data.reset_index(drop=True ,inplace = True)    
    filtered_data = filtered_data.to_dict(orient='index')
    filtered_books_by_bonus = list(filtered_data.values())

    for product in filtered_books_by_bonus:
        if (str(product['processor']) == 'nan'): product.pop('processor')            
        if (str(product['sim']) == 'nan'): product.pop('sim')
        if (str(product['camera']) == 'nan'): product.pop('camera')
        if (str(product['acc']) == 'nan'): product.pop('acc')
        if (str(product['matrix']) == 'nan'): product.pop('matrix')
        if (str(product['ram']) == 'nan'): product.pop('ram')
        if (str(product['resolution']) == 'nan'): product.pop('resolution')

    with open('task_2_filtered_products_by_bonus.json', 'w', encoding='utf-8') as file:
        json.dump(filtered_books_by_bonus, file, ensure_ascii=False, indent = 4)

charact = []

def get_numeric_charact(data):
    numeric_charact = {}
                    
    numeric_charact[f'sum_price'] = data['price'].sum()
    numeric_charact[f'max_price'] = data['price'].max()
    numeric_charact[f'min_price'] = data['price'].min()
    numeric_charact[f'mean_price'] = data['price'].mean()
    numeric_charact[f'std_price'] = data['price'].std()

    for key in numeric_charact.keys():
        if (type(numeric_charact[key]) == np.int64):
            numeric_charact[key] = int(numeric_charact[key])
        else:
            numeric_charact[key] = float(numeric_charact[key])

    charact.append(numeric_charact)

def get_categorial_charact(data):
    categorial_charact = {}
    
    for word in data['resolution']:
        if (categorial_charact.get(word) == None):
            categorial_charact[word] = 1
        else:
            categorial_charact[word] = categorial_charact[word] + 1
        
    charact.append(categorial_charact)

def get_result_in_json():
    with open('task_2_charact_result.json', 'w', encoding='utf-8') as file:
        json.dump(charact, file, ensure_ascii=False, indent = 4)


handle_file()
get_sorted(data=data)
get_filtered(data=data)
get_numeric_charact(data=data)
get_categorial_charact(data)
get_result_in_json()