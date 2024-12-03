from bs4 import BeautifulSoup
import json
import pandas as pd
import numpy as np

items = []

def handle_file():
    for filename in range (1, 126):
        with open(f'{filename}.xml', 'r', encoding='utf-8') as file:
            xml_content = file.read()
        
        soup = BeautifulSoup(xml_content, features='xml')
        
        item = {}  
        item['name'] = soup.find_all(name='name')[0].get_text(strip=True)
        item['constellation'] = soup.find_all(name='constellation')[0].get_text(strip=True)
        item['spectral-class'] = soup.find_all(name='spectral-class')[0].get_text(strip=True)
        item['radius'] = int(soup.find_all(name='radius')[0].get_text(strip=True))
        item['rotation_days'] = float(soup.find_all(name='rotation')[0].get_text(strip=True).split(" ")[0])
        item['age_billion_years'] = float(soup.find_all(name='age')[0].get_text(strip=True).split(" ")[0])
        item['distance_million_km'] = float(soup.find_all(name='distance')[0].get_text(strip=True).split(" ")[0])
        item['absolute-magnitude_million_km'] = float(soup.find_all(name='absolute-magnitude')[0].get_text(strip=True).split(" ")[0])
     
        items.append(item)

    with open('task_3_result.json', 'w', encoding='utf-8') as file:
        json.dump(items, file, ensure_ascii=False, indent = 4)

data = pd.read_json('task_3_result.json')

def get_sorted(data):
    sorted_data = data.sort_values(by=['radius'], ignore_index=True)
    sorted_data = sorted_data.to_dict(orient='index')
    sorted_stars_by_radius = list(sorted_data.values())

    with open('task_3_sorted_stars_by_radius.json', 'w', encoding='utf-8') as file:
        json.dump(sorted_stars_by_radius, file, ensure_ascii=False, indent = 4)    

def get_filtered(data):
    filtered_data = data.copy()    
    filtered_data.drop(filtered_data[filtered_data.age_billion_years < 5].index, inplace = True)
    filtered_data.reset_index(drop=True ,inplace = True)    
    filtered_data = filtered_data.to_dict(orient='index')
    filtered_stars_by_age = list(filtered_data.values())

    with open('task_3_filtered_stars_by_age.json', 'w', encoding='utf-8') as file:
        json.dump(filtered_stars_by_age, file, ensure_ascii=False, indent = 4)

charact = []

def get_numeric_charact(data):
    numeric_charact = {}
                    
    numeric_charact[f'sum_rotation'] = data['rotation_days'].sum()
    numeric_charact[f'max_rotation'] = data['rotation_days'].max()
    numeric_charact[f'min_rotation'] = data['rotation_days'].min()
    numeric_charact[f'mean_rotation'] = data['rotation_days'].mean()
    numeric_charact[f'std_rotation'] = data['rotation_days'].std()

    for key in numeric_charact.keys():
        if (type(numeric_charact[key]) == np.int64):
            numeric_charact[key] = int(numeric_charact[key])
        else:
            numeric_charact[key] = float(numeric_charact[key])

    charact.append(numeric_charact)

def get_categorial_charact(data):
    categorial_charact = {}
    
    for word in data['constellation']:
        if (categorial_charact.get(word) == None):
            categorial_charact[word] = 1
        else:
            categorial_charact[word] = categorial_charact[word] + 1
    
    charact.append(categorial_charact)

def get_result_in_json():
    with open('task_3_charact_result.json', 'w', encoding='utf-8') as file:
        json.dump(charact, file, ensure_ascii=False, indent = 4)

handle_file()

get_sorted(data=data)
get_filtered(data=data)
get_numeric_charact(data=data)
get_categorial_charact(data)
get_result_in_json()