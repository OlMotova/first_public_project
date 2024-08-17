# -*- coding: utf-8 -*-
import pandas as pd
import ipaddress
from datetime import datetime
import sys
import numpy as np
from contextlib import redirect_stdout
from ipaddress import IPv4Network

#loading start
def df_loading(file_name):
    df = pd.read_excel(file_name)
    return df

df = df_loading('Main_file.xlsx')
equipment_df = df_loading('equipment_database.xlsx')
#df = pd.read_excel('Main_file_test.xlsx')
#equipment_df = pd.read_excel('equipment_database.xlsx')

#loading end

def unique_equipment(df, column):
    unique_equipment_list = df[column].unique()
    return unique_equipment_list

print(unique_equipment(equipment_df, 'equipment_name'))
#print(equipment_df['equipment_name'].unique())
equipment_name = input("Введите (скопируйте) имя устройства: ")

def df_filter(df, column, parameter):
    df_2 = df[df[column] == parameter]
    return df_2

df_2 = df_filter(df, 'equipment_name', equipment_name)
equipment_df_2 = df_filter(equipment_df, 'equipment_name', equipment_name)

#df_2 = df[df['equipment_name'] == equipment_name]
#equipment_df_2 = equipment_df[equipment_df['equipment_name'] == equipment_name]

print(unique_equipment(equipment_df_2, 'equipment_type'))
#print(equipment_df_2['equipment_type'].unique())
equipment_type = input("Введите (скопируйте) тип устройства: ")

df_3 = df_filter(df_2, 'equipment_type', equipment_type)
equipment_df_3 = df_filter(equipment_df_2, 'equipment_type', equipment_type)

#df_3 = df_2[df_2['equipment_type'] == equipment_type]
#equipment_df_3 = equipment_df_2[equipment_df_2['equipment_type'] == equipment_type]
equipment_index = equipment_df_3.index
equipment_df_3 = equipment_df_3.reset_index(drop = True)

stickers_count = int(input("Введите колличество этикеток: "))


def new_order_creating(df_main, df_base):

    global new_first_IP
    global new_first_ZvN
    global new_last_IP
    global new_last_ZvN
    global order_number

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

    order_number = df['order_number'].max() + 1

    df_add = {
        'order_number': order_number,
        'equipment_name': equipment_name,
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
        print("Проверка пройдена: заводской номер в допустимом диапазоне")
    else:
        print(f"""ОШИБКА: заводской номер вне диапазона.
Для заказа доступно {max_ZvN - new_first_ZvN + 1} этикеток""")
        sys.exit()

    if min_IP <= new_first_IP and new_last_IP <= max_IP:
        print("Проверка пройдена: IP в допустимом диапазоне")
    else:
        print("ОШИБКА: IP вне диапазона")
        sys.exit()



equipment_index_int = int(equipment_index[0])
IP_range_check(equipment_df, equipment_index_int)

df = df._append(df_add, ignore_index= True)
#print(df.tail())

df.to_excel("Main_file.xlsx", index=False) #запись в файл


def IP_converter(IP):
    str_IP = str(IP)
    line_IP = str_IP.split('.')
    return line_IP

def middle_IP_creating(a, b, c):
    middle_IP= ipaddress.ip_address(str(a) + '.' + str(b) + '.' + str(c) + '.' + '255')
    return middle_IP

#def createList(r1, r2):
#    return list(range(r1, r2 + 1))

def create_IP_list(r1, r2):
    # Testing if range r1 and r2
    # are equal
    if (r1 == r2):
        return r1

    else:
        # Create empty list
        res = []

        # loop to append successors to
        # list until r2 is reached.
        while (r1 < (r2 + 1)):
            res.append(r1)
            r1 += 1
        return res

first_IP_parts = IP_converter(new_first_IP)
last_IP_parts = IP_converter(new_last_IP)

arrays_equal = np.array_equal(first_IP_parts[0:3], last_IP_parts[0:3])

if arrays_equal == True:
    print("Проверка пройдена: IP в одном диапазоне")
    print(f'''
________________________________________
Информация о новом заказе № {order_number} внесена в базу.

Требуется заказать этикетки для {equipment_name} {equipment_type} 
с заводскими номерами {new_first_ZvN} - {new_last_ZvN} и IP

{new_first_IP}, {new_first_IP + 1}, ..., {new_last_IP}

''')

    # Вывод 'print' отправляется в 'output.txt'
    with open('output.txt', 'w') as f, redirect_stdout(f):
        print(f'''
________________________________________
Информация о новом заказе № {order_number} внесена в базу.

Требуется заказать этикетки для {equipment_name} {equipment_type} 
с заводскими номерами {new_first_ZvN} - {new_last_ZvN} и IP

{new_first_IP}, {new_first_IP + 1}, ..., {new_last_IP}.

''')

else:
    print("\nнадо поработать над разделением диапазонов")
    middle_IP = middle_IP_creating(first_IP_parts[0], first_IP_parts[1], first_IP_parts[2])
    list_1 = create_IP_list(new_first_IP, middle_IP)
    list_2 = create_IP_list(middle_IP + 1, new_last_IP)
    print(f'''
{middle_IP}
{list_1}
{list_2}
''')
    if len(list_1) < 4 and len(list_2) < 4:
        line_1 = ', '.join(map(str, list_1))
        line_2 = ', '.join(map(str, list_2))
    elif len(list_1) < 4:
        line_1 = ', '.join(map(str, list_1))
        line_2 = str(middle_IP + 1) + ', ' + str(middle_IP + 2) + ', ... , ' + str(new_last_IP + 1)
    elif len(list_2) < 4:
        line_1 = str(new_first_IP) + ', ' + str(new_first_IP + 1) + ', ... , ' + str(middle_IP)
        line_2 = ', '.join(map(str, list_2))
    else:
        line_1 = str(new_first_IP) + ', ' + str(new_first_IP + 1) + ', ... , ' + str(middle_IP)
        line_2 = str(middle_IP + 1) + ', ' + str(middle_IP + 2) + ', ... , ' + str(new_last_IP + 1)

    print(f'''
________________________________________
Информация о новом заказе № {order_number} внесена в базу.

Требуется заказать этикетки для {equipment_name} {equipment_type} 
с заводскими номерами {new_first_ZvN} - {new_last_ZvN} и IP

{line_1}, 
{line_2}.

''')

    with open('output.txt', 'w') as f, redirect_stdout(f):
            print(f'''
________________________________________
Информация о новом заказе № {order_number} внесена в базу.

Требуется заказать этикетки для {equipment_name} {equipment_type} 
с заводскими номерами {new_first_ZvN} - {new_last_ZvN} и IP

{line_1}, 
{line_2}.

''')


#input()




