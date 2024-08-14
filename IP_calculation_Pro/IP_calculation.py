import pandas as pd
import ipaddress
import re
from datetime import datetime

#loading start

df = pd.read_excel('Main_file_test.xlsx')

#loading end

#data type convert
df['order_date'] = pd.to_datetime(df['order_date'], format='%d.%m.%Y')
#df['last_IP'] = df['last_IP'].ip.apply(lambda x: ipaddress.ip_address(x))

#print('________________________')
#print(df.dtypes)

#print(df.describe())
#print('________________________')

print(df['equipment_name'].unique())
equipment_name = input("Введите (скопируйте) имя устройства: ")
df_2 = df[df['equipment_name'] == equipment_name]

print(df_2['equipment_type'].unique())
equipment_type = input("Введите (скопируйте) тип устройства: ")
df_3 = df_2[df_2['equipment_type'] == equipment_type]
print(df_3)

print('________________________')
max_ZvN = df_3['last_serial_number'].max()
max_IP = df_3['last_IP'].max()
print(f'''Последний используемый IP: {max_IP}
Последний используемый заводской номер: {max_ZvN}''')

stickers_count = 256

if df_3['last_serial_number'].idxmax() == df_3['last_IP'].idxmax():

    IP_max_IP = ipaddress.ip_address(max_IP)
    new_max_IP = IP_max_IP + stickers_count
    new_max_ZvN = max_ZvN + stickers_count
    print(f'Новый последний IP: {new_max_IP}')

else: print("Ошибка вычисления максимального значения")

df_add = {'equipment_name': equipment_name,
'equipment_type': equipment_type,
'last_serial_number': new_max_ZvN,
'last_IP': new_max_IP,
'order_date': 'здесь будет дата'}

df = df._append(df_add, ignore_index= True)
#df.loc[ len(df.index )] = [equipment_name, 'здесь будет тип', 'здесь будет серийник', new_max_IP, 'здесь будет дата']
print(df.tail())


df.to_excel("output.xlsx")