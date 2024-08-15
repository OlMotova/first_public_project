# -*- coding: utf-8 -*-
import pandas as pd
import ipaddress
from datetime import datetime
import sys
from ipaddress import IPv4Network

#loading start
df = pd.read_excel('Main_file_test.xlsx')
equipment_df = pd.read_excel('equipment_database.xlsx')
#loading end


print(equipment_df['equipment_name'].unique())
equipment_name = input("Введите (скопируйте) имя устройства: ")
df_2 = df[df['equipment_name'] == equipment_name]
equipment_df_2 = equipment_df[equipment_df['equipment_name'] == equipment_name]

print(equipment_df_2['equipment_type'].unique())
equipment_type = input("Введите (скопируйте) тип устройства: ")
df_3 = df_2[df_2['equipment_type'] == equipment_type]
equipment_df_3 = equipment_df_2[equipment_df_2['equipment_type'] == equipment_type]
equipment_index = equipment_df_3.index
equipment_df_3 = equipment_df_3.reset_index(drop = True)

stickers_count = int(input("Введите колличество этикеток: "))


def new_order_creating(df_main, df_base):

    global new_first_IP
    global new_first_ZvN
    global new_last_IP
    global new_last_ZvN

    if df_main.empty: #работа с новым элементом

        new_first_IP_ = df_base['first_IP'][0]
        new_first_IP = ipaddress.ip_address(new_first_IP_)
        new_first_ZvN = df_base['first_serial_number'][0]
        new_last_IP = new_first_IP + stickers_count - 1
        new_last_ZvN = new_first_ZvN + stickers_count - 1


    else:
        print(df_main)
        print('________________________')
        last_ZvN = df_main['last_serial_number'].max()
        last_IP_ = df_main['last_IP'].max()
        print(f'''Последний используемый IP: {last_IP_}
        Последний используемый заводской номер: {last_ZvN}''')


        if df_main['last_serial_number'].idxmax() == df_main['last_IP'].idxmax():

            last_IP = ipaddress.ip_address(last_IP_)
            new_last_IP = last_IP + stickers_count
            new_last_ZvN = last_ZvN + stickers_count
            new_first_IP = last_IP + 1
            new_first_ZvN = last_ZvN + 1
            print(f'Новый последний IP: {new_last_IP}')

        else: print(f"""Ошибка вычисления максимального значения: 
индекс заводского номера: {df_main['last_serial_number'].idxmax()}
индекс IP: {df_main['last_IP'].idxmax()}
""")



    df_add = {'equipment_name': equipment_name,
'equipment_type': equipment_type,
'first_serial_number': new_first_ZvN,
'last_serial_number': new_last_ZvN,
'first_IP': new_first_IP,
'last_IP': new_last_IP,
'stickers_count': stickers_count,
'order_date': datetime.now()}
    return df_add

df_add = {}

if stickers_count > 2:
    df_add = new_order_creating(df_3, equipment_df_3) #запуск основной функции
elif stickers_count == 2:
    print("доработать программу для двух этикеток")
    sys.exit()
elif stickers_count == 1:
    print("доработать программу для одной этикетки")
    sys.exit()
elif stickers_count < 1:
    print("Ошибка ввода числа этикеток!")
    sys.exit()
else:
    print("Непонятная проблема!")
    sys.exit()

print(f"equipment_index.to_list: {equipment_index.to_list()}")

#if equipment_index == 8:
#    print("работает")
#else: print("фигня какая-то")

def IP_range_check(df_base, index):
    min_IP = ipaddress.ip_address(df_base['first_IP'][index])
    max_IP = ipaddress.ip_address(df_base['last_IP'][index])
    min_ZvN = df_base['first_serial_number'][index]
    max_ZvN = df_base['last_serial_number'][index]
    print(f'''
{min_IP}
{max_IP}
{min_ZvN}
{max_ZvN}
''')

    if min_ZvN <= new_first_ZvN and new_last_ZvN <= max_ZvN:
        print("заводской номер в допустимом диапазоне")
    else:
        print("ОШИБКА: заводской номер вне диапазона")
        sys.exit()

    if min_IP <= new_first_IP and new_last_IP <= max_IP:
        print("IP в допустимом диапазоне")
    else:
        print("ОШИБКА: IP вне диапазона")
        sys.exit()



equipment_index_int = int(equipment_index[0])
IP_range_check(equipment_df, equipment_index_int)


#def IP_list_exploding ():
str_first_IP = str(new_first_IP)
first_IP_parts = str_first_IP.split('.')

str_last_IP = str(new_last_IP)
last_IP_parts = str_last_IP.split('.')

for i in range(0,3):
    if first_IP_parts[i] == last_IP_parts[i]:
        print("IP в одном диапазоне")
    else: print("надо поработать над разделением диапазонов")

#IP_list_exploding()




df = df._append(df_add, ignore_index= True)
print(df.tail())







df.to_excel("Main_file_test.xlsx", index=False)
print(f'''
________________________________________
Информация о новом заказе внесена в базу.

Требуется заказать этикетки для {equipment_name} {equipment_type} 
с заводскими номерами {new_first_ZvN} - {new_last_ZvN} и IP

{new_first_IP}, {new_first_IP+1}, ..., {new_last_IP}

''')
from contextlib import redirect_stdout

# Вывод 'print' отправляется в 'output.txt'
with open('output.txt', 'w') as f, redirect_stdout(f):
    print(f'''
________________________________________
Информация о новом заказе внесена в базу.

Требуется заказать этикетки для {equipment_name} {equipment_type} 
с заводскими номерами {new_first_ZvN} - {new_last_ZvN} и IP

{new_first_IP}, {new_first_IP + 1}, ..., {new_last_IP}.

''')

