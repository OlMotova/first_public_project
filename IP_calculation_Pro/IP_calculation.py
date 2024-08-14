import pandas as pd
import ipaddress
import re
from datetime import datetime

#loading start

df = pd.read_excel('Main_file_test.xlsx')
equipment_df = pd.read_excel('equipment_database.xlsx')

#loading end

#data type convert
#df['order_date'] = pd.to_datetime(df['order_date'], format='%d.%m.%Y')
#df['last_IP'] = df['last_IP'].ip.apply(lambda x: ipaddress.ip_address(x))

#print('________________________')
#print(df.dtypes)

#print(df.describe())
#print('________________________')

print(equipment_df['equipment_name'].unique())
equipment_name = input("Введите (скопируйте) имя устройства: ")
df_2 = df[df['equipment_name'] == equipment_name]
equipment_df_2 = equipment_df[equipment_df['equipment_name'] == equipment_name]

print(equipment_df_2['equipment_type'].unique())
equipment_type = input("Введите (скопируйте) тип устройства: ")
df_3 = df_2[df_2['equipment_type'] == equipment_type]
equipment_df_3 = equipment_df_2[equipment_df_2['equipment_type'] == equipment_type]
equipment_df_3 = equipment_df_3.reset_index(drop = True)
#print(equipment_df_3.dtypes)

stickers_count = 256

if df_3.empty: #работа с новым элементом
    print('DataFrame is empty!')
#    last_ZvN = equipment_df_3['last_serial_number'][0]
#    last_IP_ = equipment_df_3['last_IP'][0]
#    last_IP = ipaddress.ip_address(last_IP_)
    new_first_IP_ = equipment_df_3['first_IP'][0]
    new_first_IP = ipaddress.ip_address(new_first_IP_)
    new_first_ZvN = equipment_df_3['first_serial_number'][0]
    new_last_IP = new_first_IP + stickers_count - 1
    new_last_ZvN = new_first_ZvN + stickers_count - 1


else:
    print(df_3)
    print('________________________')
    last_ZvN = df_3['last_serial_number'].max()
    last_IP_ = df_3['last_IP'].max()
    print(f'''Последний используемый IP: {last_IP_}
    Последний используемый заводской номер: {last_ZvN}''')


    if df_3['last_serial_number'].idxmax() == df_3['last_IP'].idxmax():

        last_IP = ipaddress.ip_address(last_IP_)
        new_last_IP = last_IP + stickers_count
        new_last_ZvN = last_ZvN + stickers_count
        new_first_IP = last_IP + 1
        new_first_ZvN = last_ZvN + 1
        print(f'Новый последний IP: {new_last_IP}')

    else: print("Ошибка вычисления максимального значения")

df_add = {'equipment_name': equipment_name,
'equipment_type': equipment_type,
'first_serial_number': new_first_ZvN,
'last_serial_number': new_last_ZvN,
'first_IP': new_first_IP,
'last_IP': new_last_IP,
'stickers_count': stickers_count,
'order_date': datetime.now()}

df = df._append(df_add, ignore_index= True)
#df.loc[ len(df.index )] = [equipment_name, 'здесь будет тип', 'здесь будет серийник', new_max_IP, 'здесь будет дата']
print(df.tail())


df.to_excel("Main_file_test.xlsx", index=False)
print(f'''
________________________________________
Информация о новом заказе внесена в базу.

Требуется заказать этикетки для {equipment_name} {equipment_type} 
с заводскими номерами {new_first_ZvN} - {new_last_ZvN} и IP

{new_first_IP}, {new_first_IP+1}, ..., {new_last_IP}

''')


