# -*- coding: utf-8 -*-
import pandas as pd
import ipaddress
from datetime import datetime
import sys
import numpy as np
from contextlib import redirect_stdout


def df_loading(file_name):  #creating a dataframe from excel file (table)
    df = pd.read_excel(file_name)
    return df

def unique_equipment(df, column):   #creating a list of unique values from the column of data frame
    unique_equipment_list = df[column].unique()
    return unique_equipment_list

def df_filter(df, column, parameter):   #filter: creaing a new data frame from the selected one by applying a filter to the selected column by the selected parameter
    df_2 = df[df[column] == parameter]
    return df_2

def index_reset(df): #resets line's index in the chosen data frame
    updated_df = df.reset_index(drop = True)
    return updated_df

def last_order_number_func (df): #returns max value in column 'order_number'
    return df['order_number'].max()

def df_preparing (df_main, df_base_IP, equipment_name, equipment_type): #creating filtered df
    df = df_main
    equipment_IP_df = df_base_IP

    df_2_0 = df_filter(df, 'ab_label', 'open')
    equipment_IP_df_2_0 = df_filter(equipment_IP_df, 'ab_label', 'open')

    df_2_1 = df_filter(df_2_0, 'equipment_name', equipment_name)
    equipment_IP_df_2_1 = df_filter(equipment_IP_df_2_0, 'equipment_name', equipment_name)

    df_2 = df_filter(df_2_1, 'equipment_type', equipment_type)
    equipment_IP_df_2 = df_filter(equipment_IP_df_2_1, 'equipment_type', equipment_type)

    return df, df_2, equipment_IP_df_2

def IP_converter(IP): #splits the IP address into segments
    str_IP = str(IP)
    line_IP = str_IP.split('.')
    return line_IP

def middle_IP_creating(a, b, c): #creating the last IP address in the section named 'middle IP'
    middle_IP= ipaddress.ip_address(str(a) + '.' + str(b) + '.' + str(c) + '.' + '255')
    return middle_IP

def create_IP_list(r1, r2): #creating a list of IP addresses for output
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

def IP_subtraction (IP_1, IP_2):

    IP_1_parts = IP_converter(IP_1)
    IP_2_parts = IP_converter(IP_2)

    arrays_equal = np.array_equal(IP_1_parts[0:2], IP_2_parts[0:2])

    if arrays_equal == True:

        n = (int(IP_2_parts[2]) - int(IP_1_parts[2])) * 256 + (int(IP_2_parts[3]) - int(IP_1_parts[3]))
        return n
    else:
        text = f"Что-то между IPшниками слишком большая разница."
        return text

def new_values_calculating (df_main, df_base, stickers_count):

    if df_main.empty:  #calculating values for a new equipment

        new_first_IP_ = df_base['first_IP'][0]
        new_first_IP = ipaddress.ip_address(new_first_IP_)
        new_first_ZvN = df_base['first_serial_number'][0]
        new_last_IP = new_first_IP + stickers_count - 1
        new_last_ZvN = new_first_ZvN + stickers_count - 1

    else: #calculation of values for the equipment found in the table Main_file
        print(df_main)
        print('________________________')
        last_ZvN = df_main['last_serial_number'].max()
        last_line = df_main['last_serial_number'].idxmax()
        last_IP_ = df_main.loc[last_line, 'last_IP']

        print(f'''Последний используемый IP: {last_IP_}
Последний используемый заводской номер: {last_ZvN}
''')

        # if df_main['last_serial_number'].idxmax() != df_main['last_IP'].idxmax():
        #     print(f"""Предупреждени! Ошибка вычисления максимального значения:
        #     индекс заводского номера - {df_main['last_serial_number'].idxmax()}
        #     индекс IP - {df_main['last_IP'].idxmax()}
        #     """)

        last_IP = ipaddress.ip_address(last_IP_)
        new_last_IP = last_IP + stickers_count
        new_last_ZvN = last_ZvN + stickers_count
        new_first_IP = last_IP + 1
        new_first_ZvN = last_ZvN + 1
        print(f"""
_______________
new_last_IP: {new_last_IP}
new_last_ZvN: {new_last_ZvN}
_______________
""")

    last_base_IP = ipaddress.ip_address(df_base['last_IP'][0])

    if new_last_IP < last_base_IP:
        ab_label = 'open'
    elif new_last_IP == last_base_IP:
        ab_label = 'close'
    else:
        print('ОЩИБКА ЭТИКЕТКИ')
        ab_label = 'error'


    return new_first_ZvN, new_last_ZvN, new_first_IP, new_last_IP, ab_label

def new_df_line_creating(order_number, equipment_name, equipment_type, equipment_version, new_first_ZvN, new_last_ZvN, new_first_IP, new_last_IP, stickers_count, ab_label): #Returns df line with new data for adding to main file

    df_add = {
        'order_number': order_number,
        'equipment_name': equipment_name,
        'equipment_type': equipment_type,
        'equipment_version': equipment_version,
        'first_serial_number': new_first_ZvN,
        'last_serial_number': new_last_ZvN,
        'first_IP': new_first_IP,
        'last_IP': new_last_IP,
        'stickers_count': stickers_count,
        'order_date': datetime.now(),
        'ab_label': ab_label}
    return df_add

def base_update (df_base, index):
    df_base.at[index, 'ab_label'] = 'close'
    df_base.to_excel("equipment_IP_database.xlsx", index=False)

def next_index_func (df):
    index_list = df.index.tolist()

    print(f'СПИСОК ИНДЕКСОВ - {index_list}')

    len_index_list = len(index_list)

    if len_index_list >= 2:
        ind = index_list[1]
        return ind

    else:
        text = "ЭТО ПОСЛЕДНИЙ ДОСТУПНЫЙ ДИАПАЗОН"
        return text


def IP_range_check_and_text_output (df_base, index, index_next, new_first_ZvN, new_last_ZvN, new_first_IP, new_last_IP, order_number, equipment_name, equipment_type, equipment_version, flag):
#checks whether the IP address belongs to a valid range AND creating text fild for output

    #check part
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
        if isinstance(index_next,int) == True :
            text = f"""ОШИБКА: заводской номер вне диапазона.
Для заказа доступно {max_ZvN - new_first_ZvN + 1} этикеток из этого диапазона,

а потом вы можете задействовать следующий: {df_base['first_IP'][index_next]} - {df_base['last_IP'][index_next]}

"""

        else:
            text = f"""ОШИБКА: заводской номер вне диапазона.
Для заказа доступно {max_ZvN - new_first_ZvN + 1} этикеток"""
        print(text)
        return text, False

    if min_IP <= new_first_IP and new_last_IP <= max_IP:
        print("Проверка пройдена: IP в допустимом диапазоне")
    else:
        text = "ОШИБКА: IP вне диапазона"
        print(text)
        return text, False

    #text part
    first_IP_parts = IP_converter(new_first_IP)
    last_IP_parts = IP_converter(new_last_IP)

    arrays_equal = np.array_equal(first_IP_parts[0:3], last_IP_parts[0:3])
    if arrays_equal == True:
#    if first_IP_parts[0:3] == last_IP_parts[0:3]:
        print("Проверка пройдена: IP в одном диапазоне")

        if flag == 'save_flag':
            text = f'''
Заказ № {order_number}.

Оборудование: {equipment_name} {equipment_type} {equipment_version}

Требуемый диапазон:

{new_first_ZvN} - {new_first_IP}, {new_first_ZvN + 1} - {new_first_IP + 1}, ..., {new_last_ZvN} - {new_last_IP}

________________________________________
Информация о новом заказе № {order_number} внесена в базу.    
'''
            filename = datetime.now().strftime(f"Order_{order_number}_%Y-%m-%d_%H-%M-%S.txt")

            with open(filename, 'w') as f, redirect_stdout(f):
                 print(f'''
Заказ № {order_number}.

Оборудование: {equipment_name} {equipment_type} {equipment_version}

Требуемый диапазон:

{new_first_ZvN} - {new_first_IP}, {new_first_ZvN + 1} - {new_first_IP + 1}, ..., {new_last_ZvN} - {new_last_IP}

________________________________________
Информация о новом заказе № {order_number} внесена в базу.  
''')

        else:
            text = f'''
        
Результат расчета этикеток для {equipment_name} {equipment_type} {equipment_version}:

{new_first_ZvN} - {new_first_IP}, {new_first_ZvN + 1} - {new_first_IP + 1}, ..., {new_last_ZvN} - {new_last_IP}

'''
        print(text)
        return text, True

    elif int(last_IP_parts[2]) - int(first_IP_parts[2]) == 1:
        print(f"ОТДЕЛЬНЫЕ части  {int(first_IP_parts[2])}, {int(last_IP_parts[2])}, {int(last_IP_parts[2]) - int(first_IP_parts[2])}")
        print("\nнадо поработать над разделением диапазонов")
        middle_IP = middle_IP_creating(first_IP_parts[0], first_IP_parts[1], first_IP_parts[2])
        part_of_stickers_count = 255 - int(first_IP_parts[3])
        middle_ZvN = new_first_ZvN + part_of_stickers_count

        list_IP_1 = create_IP_list(new_first_IP, middle_IP)
        list_IP_2 = create_IP_list(middle_IP + 1, new_last_IP)

        list_ZvN_1 = create_IP_list(new_first_ZvN, middle_ZvN)
        list_ZvN_2 = create_IP_list(middle_ZvN + 1, new_last_ZvN)


        list_1 = [' - '.join(x) for x in zip(map(str, list_ZvN_1), map(str, list_IP_1))]
        list_2 = [' - '.join(x) for x in zip(map(str, list_ZvN_2), map(str, list_IP_2))]
        print(f'''
    {middle_IP}
    {list_1}
    {list_2}
    ''')
        if len(list_IP_1) < 4 and len(list_IP_2) < 4:
            line_1 = ', '.join(map(str, list_1))
            line_2 = ', '.join(map(str, list_2))
        elif len(list_IP_1) < 4:
            line_1 = ', '.join(map(str, list_1))
            line_2 = f'{middle_ZvN + 1} - {middle_IP + 1}, {middle_ZvN + 2} - {middle_IP + 2}, ... , {new_last_ZvN} - {new_last_IP}'
            #line_2 = str(middle_IP + 1) + ', ' + str(middle_IP + 2) + ', ... , ' + str(new_last_IP + 1)
        elif len(list_IP_2) < 4:
            #line_1 = str(new_first_IP) + ', ' + str(new_first_IP + 1) + ', ... , ' + str(middle_IP)
            line_1 = f'{new_first_ZvN} - {new_first_IP}, {new_first_ZvN + 1} - {new_first_IP + 1}, ... , {middle_ZvN} - {middle_IP}'
            line_2 = ', '.join(map(str, list_2))
        else:
            #line_1 = str(new_first_IP) + ', ' + str(new_first_IP + 1) + ', ... , ' + str(middle_IP)
            #line_2 = str(middle_IP + 1) + ', ' + str(middle_IP + 2) + ', ... , ' + str(new_last_IP + 1)
            line_1 = f'{new_first_ZvN} - {new_first_IP}, {new_first_ZvN + 1} - {new_first_IP + 1}, ... , {middle_ZvN} - {middle_IP}'
            line_2 = f'{middle_ZvN + 1} - {middle_IP + 1}, {middle_ZvN + 2} - {middle_IP + 2}, ... , {new_last_ZvN} - {new_last_IP}'

        if flag == 'save_flag':
            text = f'''
Заказ № {order_number}.

Оборудование: {equipment_name} {equipment_type} {equipment_version}

Требуемый диапазон:

{line_1}, 
{line_2}.    

________________________________________
Информация о новом заказе № {order_number} внесена в базу.    
'''
            filename = datetime.now().strftime(f"Order_{order_number}_%Y-%m-%d_%H-%M-%S.txt")

            with open(filename, 'w') as f, redirect_stdout(f):
                print(f'''
Заказ № {order_number}.

Оборудование: {equipment_name} {equipment_type} {equipment_version}

Требуемый диапазон:

{line_1}, 
{line_2}. 

________________________________________
Информация о новом заказе № {order_number} внесена в базу.  
''')
        else:

            text = f'''
    
    Результат расчета этикеток для {equipment_name} {equipment_type} {equipment_version}:
    
    {line_1}, 
    {line_2}.
    
        '''

    elif int(last_IP_parts[2]) - int(first_IP_parts[2]) == 2:
        print(
            f"ОТДЕЛЬНЫЕ части  {int(first_IP_parts[2])}, {int(last_IP_parts[2])}, {int(last_IP_parts[2]) - int(first_IP_parts[2])}")
        print("\nнадо поработать над разделением диапазонов")
        middle_IP_1 = middle_IP_creating(first_IP_parts[0], first_IP_parts[1], first_IP_parts[2])
        part_of_stickers_count = 255 - int(first_IP_parts[3])
        middle_ZvN_1 = new_first_ZvN + part_of_stickers_count

        middle_IP_2 = middle_IP_creating(first_IP_parts[0], first_IP_parts[1], int(first_IP_parts[2]) + 1)

        middle_ZvN_2 = new_first_ZvN + part_of_stickers_count + 256


        list_IP_1 = create_IP_list(new_first_IP, middle_IP_1)
        list_IP_2 = create_IP_list(middle_IP_1 + 1, middle_IP_2)
        list_IP_3 = create_IP_list(middle_IP_2 + 1, new_last_IP)

        list_ZvN_1 = create_IP_list(new_first_ZvN, middle_ZvN_1)
        list_ZvN_2 = create_IP_list(middle_ZvN_1 + 1, middle_ZvN_2)
        list_ZvN_3 = create_IP_list(middle_ZvN_2 + 1, new_last_ZvN)

        list_1 = [' - '.join(x) for x in zip(map(str, list_ZvN_1), map(str, list_IP_1))]
        list_2 = [' - '.join(x) for x in zip(map(str, list_ZvN_2), map(str, list_IP_2))]
        list_3 = [' - '.join(x) for x in zip(map(str, list_ZvN_3), map(str, list_IP_3))]
        print(f'''
        {middle_IP_1} - {middle_IP_2}
        {list_1}
        {list_2}
        {list_3}
        ''')
        if len(list_IP_1) < 4 and len(list_IP_3) < 4:
            line_1 = ', '.join(map(str, list_1))
            line_2 = f'{middle_ZvN_1 + 1} - {middle_IP_1 + 1}, {middle_ZvN_1 + 2} - {middle_IP_1 + 2}, ... , {middle_ZvN_2} - {middle_IP_2}'
            line_3 = ', '.join(map(str, list_3))
        elif len(list_IP_1) < 4:
            line_1 = ', '.join(map(str, list_1))
            line_2 = f'{middle_ZvN_1 + 1} - {middle_IP_1 + 1}, {middle_ZvN_1 + 2} - {middle_IP_1 + 2}, ... , {middle_ZvN_2} - {middle_IP_2}'
            line_3 = f'{middle_ZvN_2 + 1} - {middle_IP_2 + 1}, {middle_ZvN_2 + 2} - {middle_IP_2 + 2}, ... , {new_last_ZvN} - {new_last_IP}'
        elif len(list_IP_2) < 4:
            line_1 = f'{new_first_ZvN} - {new_first_IP}, {new_first_ZvN + 1} - {new_first_IP + 1}, ... , {middle_ZvN_1} - {middle_IP_1}'
            line_2 = f'{middle_ZvN_1 + 1} - {middle_IP_1 + 1}, {middle_ZvN_1 + 2} - {middle_IP_1 + 2}, ... , {middle_ZvN_2} - {middle_IP_2}'
            line_3 = ', '.join(map(str, list_3))
        else:
            line_1 = f'{new_first_ZvN} - {new_first_IP}, {new_first_ZvN + 1} - {new_first_IP + 1}, ... , {middle_ZvN_1} - {middle_IP_1}'
            line_2 = f'{middle_ZvN_1 + 1} - {middle_IP_1 + 1}, {middle_ZvN_1 + 2} - {middle_IP_1 + 2}, ... , {middle_ZvN_2} - {middle_IP_2}'
            line_3 = f'{middle_ZvN_2 + 1} - {middle_IP_2 + 1}, {middle_ZvN_2 + 2} - {middle_IP_2 + 2}, ... , {new_last_ZvN} - {new_last_IP}'

        if flag == 'save_flag':
            text = f'''
Заказ № {order_number}.

Оборудование: {equipment_name} {equipment_type} {equipment_version}

Требуемый диапазон:

{line_1}, 
{line_2},
{line_3}.  

________________________________________
Информация о новом заказе № {order_number} внесена в базу.    
'''
            filename = datetime.now().strftime(f"Order_{order_number}_%Y-%m-%d_%H-%M-%S.txt")

            with open(filename, 'w') as f, redirect_stdout(f):
                print(f'''
Заказ № {order_number}.

Оборудование: {equipment_name} {equipment_type} {equipment_version}

Требуемый диапазон:

{line_1}, 
{line_2},
{line_3}.

________________________________________
Информация о новом заказе № {order_number} внесена в базу.  
''')
        else:
            text = f'''

Результат расчета этикеток для {equipment_name} {equipment_type} {equipment_version}:

{line_1}, 
{line_2},
{line_3}.

'''


    else:

        text = 'А не дофига ли???'
        #text = f"ВНИМАНИЕ!!! {int(first_IP_parts[2])}, {int(last_IP_parts[2])}, {int(last_IP_parts[2]) - int(first_IP_parts[2])}"
        return text, False

    print(text)
    return text, True



def calculating_button(df_main, df_base_IP, equipment_name, equipment_type, equipment_version, stickers_count):

    df, df_2, equipment_IP_df_2 = df_preparing(df_main, df_base_IP, equipment_name, equipment_type)

    if equipment_IP_df_2.empty:
        text = "НЕТ СВОБОДНОГО ДИАПАЗОНА"
        print("НЕТ СВОБОДНОГО ДИАПАЗОНА")
        return text, False

    equipment_index = equipment_IP_df_2.index #would be used for range check
    index_next = next_index_func(equipment_IP_df_2)
    print(f'index_next!!!! = {index_next}')
    equipment_IP_df_2 = index_reset(equipment_IP_df_2)



    equipment_index_int = int(equipment_index[0])

    new_first_ZvN, new_last_ZvN, new_first_IP, new_last_IP, ab_label = new_values_calculating (df_2, equipment_IP_df_2, stickers_count)

    last_order_number = last_order_number_func(df)
    order_number = last_order_number + 1

    function_flag = 'calculation_flag'
    text, flag = IP_range_check_and_text_output(df_base_IP, equipment_index_int, index_next, new_first_ZvN, new_last_ZvN, new_first_IP, new_last_IP, order_number, equipment_name, equipment_type, equipment_version, function_flag)

    print(f"""
____________________________________________    
функция отработала и получила значения
TEXT {text}

FLAG {flag}
""")
    return text, flag


def save_button (df_main, df_base_IP, equipment_name, equipment_type, equipment_version, stickers_count):

    df, df_2, equipment_IP_df_2 = df_preparing(df_main, df_base_IP, equipment_name, equipment_type)

    if equipment_IP_df_2.empty:
        text = "НЕТ СВОБОДНОГО ДИАПАЗОНА"
        return text, False


    equipment_index = equipment_IP_df_2.index #would be used for range check
    index_next = next_index_func(equipment_IP_df_2)
    print(f'index_next!!!! = {index_next}')
    equipment_IP_df_3 = index_reset(equipment_IP_df_2)



    equipment_index_int = int(equipment_index[0])

    new_first_ZvN, new_last_ZvN, new_first_IP, new_last_IP, ab_label = new_values_calculating (df_2, equipment_IP_df_3, stickers_count)

    last_order_number = last_order_number_func(df)
    order_number = last_order_number + 1

    function_flag = 'save_flag'
    text, flag = IP_range_check_and_text_output(df_base_IP, equipment_index_int, index_next, new_first_ZvN, new_last_ZvN, new_first_IP, new_last_IP, order_number, equipment_name, equipment_type, equipment_version, function_flag)

    print(f"""
____________________________________________    
функция отработала и получила значения
TEXT {text}

""")
    if ab_label == 'close':

        equipment_df_2_current = equipment_IP_df_2.loc[equipment_IP_df_2['first_serial_number'] <= new_last_ZvN]
        main_index = df_2.index.tolist()  # would be used for Main_file update
        base_index = equipment_df_2_current.index.tolist() # would be used for base file update

        print(main_index)
        print(base_index)

        for i in list(main_index):
            df.at[i, 'ab_label'] = 'close'

        for j in list(base_index):

            df_base_IP.at[j, 'ab_label'] = 'close'

        df_base_IP.to_excel("equipment_IP_database.xlsx", index=False)

    if ab_label == 'error':
        text = 'ОШИБКА ЛЕЙБЛА'
        return text

    df_add = {}

    df_add = new_df_line_creating(order_number, equipment_name, equipment_type, equipment_version, new_first_ZvN, new_last_ZvN, new_first_IP, new_last_IP, stickers_count, ab_label)
    df = df._append(df_add, ignore_index=True)

    df.to_excel("Main_file.xlsx", index=False) #save new line to file

    print(f'ab_label - {ab_label}')

    return text

