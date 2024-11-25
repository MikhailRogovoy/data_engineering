import json
import msgpack
import os.path

data = []

with open('third_task.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

dict = {}

for product in data:
    item = list(product.values())
    if (dict.get(item[0]) != None):
        dict[item[0]]['sum'] = item[1] + dict[item[0]]['sum']
        dict[item[0]]['count'] = 1 + dict[item[0]]['count']
        dict[item[0]]['avg_price'] = dict[item[0]]['sum'] / dict[item[0]]['count']
        if (dict[item[0]]['max_price'] < item[1]):
            dict[item[0]]['max_price'] = item[1]
        if (dict[item[0]]['min_price'] > item[1]):
            dict[item[0]]['min_price'] = item[1]
    else:        
        dict[item[0]] = {'sum' : item[1],
                         'count' : 1,
                         'avg_price' : item[1], 
                         'max_price' : item[1], 
                         'min_price' : item[1]
                        }

for product in list(dict.keys()):
    dict[product].pop('sum')
    dict[product].pop('count')

with open('third_task_result.json', 'w', encoding='utf-8') as file:
    json.dump(dict, file, ensure_ascii = False, indent = 4)

with open('third_task_result.msgpack', 'wb') as file:
    msgpack.pack(dict, file)

json_size = os.path.getsize('third_task_result.json')
msgpack_size = os.path.getsize('third_task_result.msgpack')

print(f"json_size: {json_size}")
print(f"msgpack_size: {msgpack_size}")
print(f"diff = {json_size - msgpack_size}")