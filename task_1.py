from bs4 import BeautifulSoup
import json
import pandas as pd
import numpy as np

items = []

def handle_file():
    for filename in range (2, 51):
        with open(f'{filename}.html', 'r', encoding='utf-8') as file:
            html_content = file.read()
        
        soup = BeautifulSoup(html_content, features='html.parser')

        item = {}  
        item['category'] = soup.find_all(name='span')[0].get_text(strip=True).split(":")[1].strip()
        item['title'] = soup.find_all(name='h1')[0].get_text(strip=True)
        item['author'] = soup.find_all(name='p')[0].get_text(strip=True)
        item['volume'] = int(soup.find_all(name='span')[1].get_text(strip=True).split(" ")[1])
        item['year'] = int(soup.find_all(name='span')[2].get_text(strip=True).split(" ")[2])
        item['ISBN'] = soup.find_all(name='span')[3].get_text(strip=True).split(":")[1]
        item['description'] = soup.find_all(name='p')[1].get_text(strip=True).split("Описание")[1].strip()
        item['img'] = soup.img['src']
        item['rating'] = float(soup.find_all(name='span')[4].get_text(strip=True).split(":")[1])
        item['views'] = int(soup.find_all(name='span')[5].get_text(strip=True).split(":")[1])
        items.append(item)

    with open('task_1_result.json', 'w', encoding='utf-8') as file:
        json.dump(items, file, ensure_ascii=False, indent = 4)

data = pd.read_json('task_1_result.json')

def get_sorted(data):
    sorted_data = data.sort_values(by=['rating'], ignore_index=True)
    sorted_data = sorted_data.to_dict(orient='index')
    sorted_books_by_rating = list(sorted_data.values())
    
    for book in sorted_books_by_rating:
        book['rating'] = round(book['rating'], 1)

    with open('task_1_sorted_books_by_rating.json', 'w', encoding='utf-8') as file:
        json.dump(sorted_books_by_rating, file, ensure_ascii=False, indent = 4)    

def get_filtered(data):
    filtered_data = data.copy()    
    filtered_data.drop(filtered_data[filtered_data.views < 60000].index, inplace = True)
    filtered_data.reset_index(drop=True ,inplace = True)    
    filtered_data = filtered_data.to_dict(orient='index')
    filtered_books_by_views = list(filtered_data.values())

    for book in  filtered_books_by_views:
        book['rating'] = round(book['rating'], 1)

    with open('task_1_filtered_books_by_views.json', 'w', encoding='utf-8') as file:
        json.dump(filtered_books_by_views, file, ensure_ascii=False, indent = 4)

charact = []

def get_numeric_charact(data):
    numeric_charact = {}
                    
    numeric_charact[f'sum_volume'] = data['volume'].sum()
    numeric_charact[f'max_volume'] = data['volume'].max()
    numeric_charact[f'min_volume'] = data['volume'].min()
    numeric_charact[f'mean_volume'] = data['volume'].mean()
    numeric_charact[f'std_volume'] = data['volume'].std()

    for key in numeric_charact.keys():
        if (type(numeric_charact[key]) == np.int64):
            numeric_charact[key] = int(numeric_charact[key])
        else:
            numeric_charact[key] = float(numeric_charact[key])

    charact.append(numeric_charact)

def get_categorial_charact(data):
    categorial_charact = {}
    
    for word in data['category']:
        if (categorial_charact.get(word) == None):
            categorial_charact[word] = 1
        else:
            categorial_charact[word] = categorial_charact[word] + 1
    
    charact.append(categorial_charact)

def get_result_in_json():
    with open('task_1_charact_result.json', 'w', encoding='utf-8') as file:
        json.dump(charact, file, ensure_ascii=False, indent = 4)

handle_file()
get_sorted(data=data)
get_filtered(data=data)
get_numeric_charact(data=data)
get_categorial_charact(data)
get_result_in_json()