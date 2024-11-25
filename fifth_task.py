import numpy as np
import pandas as pd
import json
import msgpack
import os.path

df = pd.read_csv('fifth_task.csv', sep=',', encoding='utf-8')
df.drop(labels=['Sales Channel', 'Order Date', 'Order ID', 'Ship Date', 'Total Cost', 'Total Profit', 'Total Revenue'], axis=1, inplace=True)

charact = []

def get_numeric_charact():
    numeric_charact = {}
    numeric_list = ['Units Sold', 'Unit Price', 'Unit Cost']

    for numeric in numeric_list:              
        numeric_charact[f'sum_{numeric}'] = df[f'{numeric}'].sum()
        numeric_charact[f'max_{numeric}'] = df[f'{numeric}'].max()
        numeric_charact[f'min_{numeric}'] = df[f'{numeric}'].min()
        numeric_charact[f'mean_{numeric}'] = df[f'{numeric}'].mean()
        numeric_charact[f'std_{numeric}'] = df[f'{numeric}'].std()

    for key in numeric_charact.keys():
        if (type(numeric_charact[key]) == np.int64):
            numeric_charact[key] = int(numeric_charact[key])
        else:
            numeric_charact[key] = float(numeric_charact[key])

    charact.append(numeric_charact)

def get_categorial_charact():
    categorial_charact = {}
    categorial_list = ['Region', 'Country', 'Item Type', 'Order Priority']
    
    for categorial in categorial_list:
        for word in df[f'{categorial}']:
            if (categorial_charact.get(word) == None):
                categorial_charact[word] = 1
            else:
                categorial_charact[word] = categorial_charact[word] + 1
    
    charact.append(categorial_charact)

def get_result_in_json():
    with open('fifth_task_result.json', 'w', encoding='utf-8') as file:
        json.dump(charact, file, indent = 4)

def get_df_in_csv_json_pickle():
    df.to_csv('fifth_task_df_csv_result.csv', sep=',', encoding='utf-8', index=False)
    df.to_json('fifth_task_df_json_result.json', force_ascii=False)
    df.to_pickle('fifth_task_df_pkl_result.pkl')

def get_df_in_msgpack():
    with open('fifth_task_df_json_result.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    with open('fifth_task_df_msgpack_result.msgpack', 'wb') as file:  
        msgpack.pack(data, file)

def get_sizes_info():
    csv_size = os.path.getsize('fifth_task_df_csv_result.csv')
    json_size = os.path.getsize('fifth_task_df_json_result.json')
    pickle_size = os.path.getsize('fifth_task_df_pkl_result.pkl')
    msgpack_size = os.path.getsize('fifth_task_df_msgpack_result.msgpack')

    print(f"csv_size: {csv_size}")
    print(f"json_size: {json_size}")
    print(f"pickle_size: {pickle_size}")
    print(f"msgpack_size: {msgpack_size}")
 
get_numeric_charact()
get_categorial_charact()
get_result_in_json()
get_df_in_csv_json_pickle()
get_df_in_msgpack()
get_sizes_info()