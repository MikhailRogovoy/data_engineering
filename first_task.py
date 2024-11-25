import numpy as np
import json

matrix = np.load('first_task.npy', 'r')

def get_json_file():
    sum = int(np.sum(matrix))
    avg = float(np.mean(matrix))

    MD = matrix.diagonal()
    sumMD = int(np.sum(MD))
    avgMD = float(np.mean(MD))

    SD = np.flipud(matrix).diagonal()
    sumSD = int(np.sum(SD))
    avgSD = float(np.mean(SD))

    max = int(np.max(matrix))
    min = int(np.min(matrix))

    data = {'sum': sum, 
            'avg': avg,
            'sumMD': sumMD,
            'avgMD': avgMD,
            'sumSD': sumSD,
            'avgSD': avgSD,
            'max': max,
            'min': min        
            }

    with open('first_task.json', 'w') as file:
        json.dump(data, file)

def get_normalized_matrix():
    sum = np.sum(matrix)
    normalized_matrix = matrix / sum   
    np.save('first_task_normalized_matrix', normalized_matrix)

get_json_file()
get_normalized_matrix()