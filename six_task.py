import json
from bs4 import BeautifulSoup

#https://www.w3schools.io/json-sample-examples/
json_example = """
{
   "employees":[
      {
         "name":"John",
         "salary":1,
         "department":"sales",
         "active": true
      },{
         "name": "Eric",
         "salary":12,
         "department": "marketing",
         "active": true
      },
      {
         "name": "David",
         "salary":2,
         "department": "HR",
         "active": true
      }
   ]
}                
"""
items = json.loads(json_example)
soup = BeautifulSoup(markup="", features='html.parser')
employees_table = soup.new_tag(name='table', id='employees')

def make_header():    
    thead = soup.new_tag('thead')
    employees_table.append(thead)
    tr = soup.new_tag('tr')    
    thead.append(tr)
    headers = items['employees'][0].keys()    

    for header in headers:
        th = soup.new_tag('th')
        th.string = header
        tr.append(th)

def make_content():    
    tbody = soup.new_tag('tbody')
    employees_table.append(tbody)    

    for dict in items['employees']:
        tr = soup.new_tag('tr')
        tbody.append(tr)        
        for content in dict.values():
            td = soup.new_tag('td')
            td.string = f"{content}"
            tr.append(td)

def get_result():
    with open('six_task_result.html', 'w', encoding='utf-8') as f:
        f.write(employees_table.prettify())

make_header()
make_content()
get_result()