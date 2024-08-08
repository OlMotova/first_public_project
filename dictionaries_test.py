dict_sample = {
  "Company": "Toyota",
  "model": "Premio",
  "year": 2012
}
print(dict_sample)

x = dict_sample["model"]
print(f'model is {x}')

dict = {'Name': 'Mercy', 'Age': 23, 'Course': 'Accounting'}
print("Student Name:", dict['Name'])
print("Course:", dict['Course'])
print("Age:", dict['Age'])


print(f"Student Name is {dict['Name']}")

dict_sample["Capacity"] = "1800CC"
print(dict_sample)

print('________________________________________')

import json
try:
    with open('config.json', 'r', encoding='utf-8') as json_file:
        #data = json.load(json_file)
        dict_sample = json.load(json_file)
except FileNotFoundError:
    #data = {}
    dict_sample = {}
print(dict_sample)
print('************************')
x = dict_sample.keys()

print(x)

for k in dict_sample.keys():
    print(k)

print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
a = dict_sample["cars"]
b = dict_sample["mirrors"]
print(f"""
cars: {a}
mirrors: {b}
""")

try:
    for i in range(0,11):
        print(f'значение {i}: {a[i]}')
except:
    print("STOP")

for i in range(0,9):
    print(a[i].keys())
print('################################')
for key, value in a[1].items():
    print(key, value)

for i in range(0,9):
    print(f'name {i} - {a[i]["name"]}')
    print(f'button {i} - {a[i]["button"]}')
print('0_0_0_0_0_0_0')
try:
    for i in range(1,11):
        for j in range(0,2):
            print(f'значение layout {i}--{j}: {a[i]["layouts"][j]}')
except:
    print("STOP")

print(a[1]["layouts"][1].keys())
print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')

try:
    for i in range(0,20):
        print(f'значение {i}: {a[1]["layouts"][1]['cams'][i]}')
except:
    print("STOP")

for key, value in a[1]["layouts"][1]['cams'][1].items():
    print(key, value)

print(f"""

dict_sample["cars"][1]["layouts"][1]['cams'][1]['comment'] = {dict_sample["cars"][1]["layouts"][1]['cams'][1]['comment']}

""")