import json
try:
    with open('config.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
except FileNotFoundError:
    data = {}
#print('************************')
print(data.keys())
print('0000000')
for i in range(0,4):
    print(f'''
data['cars'][0]['name'] = {data['cars'][0]['name']},
data['cars'][0]['button'] = {data['cars'][0]['button']},
data['cars'][0]['layouts'][0]['cams'][{i}]['comment'] = {data['cars'][0]['layouts'][0]['cams'][i]['comment']},
data['cars'][0]['layouts'][0]['cams'][{i}]['url'] = {data['cars'][0]['layouts'][0]['cams'][i]['url']},
data['cars'][0]['layouts'][0]['cams'][{i}]['win'] = {data['cars'][0]['layouts'][0]['cams'][i]['win']}
''')
print('12341234')
try:
    for i in range(1,9):
        for j in range(0,2):
            for k in range(0,4):
                print(f'''
data['cars'][{i}]['name'] = {data['cars'][i]['name']},
data['cars'][{i}]['button'] = {data['cars'][i]['button']},
data['cars'][{i}]['layouts'][{j}]['cams'][{k}]['comment'] = {data['cars'][i]['layouts'][j]['cams'][k]['comment']},
data['cars'][{i}]['layouts'][{j}]['cams'][{k}]['url'] = {data['cars'][i]['layouts'][j]['cams'][k]['url']},
data['cars'][{i}]['layouts'][{j}]['cams'][{k}]['win'] = {data['cars'][i]['layouts'][j]['cams'][k]['win']}.

data['cars'][{i}]['sidepanel'][{k}][{j}]['comment'] = {data['cars'][i]['sidepanel'][k][j]['comment']},
data['cars'][{i}]['sidepanel'][{k}][{j}]['url'] = {data['cars'][i]['sidepanel'][k][j]['url']},
data['cars'][{i}]['sidepanel'][{k}][{j}]['win'] = {data['cars'][i]['sidepanel'][k][j]['win']}.
''')


except: print('ERROR')

print('99999999')
for i in range(0,4):
    print(f'''
data['cars'][9]['name'] = {data['cars'][0]['name']},
data['cars'][9]['button'] = {data['cars'][0]['button']},
data['cars'][9]['layouts'][0]['cams'][{i}]['comment'] = {data['cars'][9]['layouts'][0]['cams'][i]['comment']},
data['cars'][9]['layouts'][0]['cams'][{i}]['url'] = {data['cars'][9]['layouts'][0]['cams'][i]['url']},
data['cars'][9]['layouts'][0]['cams'][{i}]['win'] = {data['cars'][9]['layouts'][0]['cams'][i]['win']}
''')


