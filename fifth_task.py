from bs4 import BeautifulSoup
import csv

def read_html_file():
    with open('fifth_task.html', 'r', encoding="utf-8") as file:
        textfile = file.read()
    return textfile

def get_headers():    
    html_file = read_html_file()
    headers = []
    soup = BeautifulSoup(html_file, "html.parser")

    for raw in soup.thead.find_all('tr'):       
       for column in raw.find_all('th'):
            headers.extend(column.contents)

    return headers

def get_data():    
    html_file = read_html_file()
    data = []
    soup = BeautifulSoup(html_file, "html.parser")

    for raw in soup.tbody.find_all('tr'): 
        raws = []     
        for column in raw.find_all('td'):            
            raws.extend(column.contents)
        data.append(raws)
    
    return data

def get_csv():    
    header = get_headers()    
    data = get_data()
    data.insert(0, header)
    
    with open('fifth_task_result.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=',')        
        writer.writerows(data)

get_csv()       