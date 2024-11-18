from pandas import read_csv
from statistics import mean

def get_dataframe():
    df = read_csv('fourth_task.txt', sep=',')
    return df

def get_avarage_max_min():
    df = get_dataframe()
    avg_rating = mean(df['rating'])
    max_price = max(df['price'])
    min_quantity = min(df['quantity'])

    with open('fourth_task_result.txt', 'w', encoding='utf-8') as f:
        f.write(f"{avg_rating}" + "\n")
        f.write(f"{max_price}" "\n")
        f.write(f"{min_quantity}" "\n")

def get_modify_file():
    df = get_dataframe()
    df.drop(labels='description', axis=1, inplace=True)
    df.drop(df[df['price'] > 6722].index, inplace=True)
    df.to_csv('fourth_task_modify_result.csv', sep=',', index=False)

get_avarage_max_min()
get_modify_file()