import pickle
import json

with open('fourth_task_products.json', 'rb') as file:
    products = pickle.load(file)

with open('fourth_task_updates.json', 'r', encoding='utf-8') as file:
    updates = json.load(file)

methods = { 'add' : lambda price, param: price + param,
            'sub' : lambda price, param: price - param,
            'percent+' : lambda price, param: price * (1+param),
            'percent-' : lambda price, param: price * (1-param)
          }

modify_products = products.copy()

for update in updates:
    for i in range(len(modify_products)):
        if update['name'] == modify_products[i]['name']:
            method = update['method']
            price = modify_products[i]['price']
            param = update['param']
            modify_products[i]['price'] = methods[method](price, param)            

with open('fourth_task_modify_products.pkl', 'wb') as file:
    pickle.dump(modify_products, file)