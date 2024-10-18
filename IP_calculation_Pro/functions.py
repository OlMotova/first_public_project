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

def df_filter(df, column, parameter):   #filter: creating a new data frame from the selected one by applying a filter to the selected column by the selected parameter
    df_2 = df[df[column] == parameter]
    return df_2

def index_reset(df): #resets line's index in the chosen data frame
    updated_df = df.reset_index(drop = True)
    return updated_df

def last_order_number_func (df):
    return df['order_number'].max()

#main function
def new_order_creating(df_main, df_base, stickers_count, last_order_number, equipment_name, equipment_type):
#the main function. Return df line with new data for adding to main file

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
        last_line = df_main['last_serial_number'].idxmax()
        last_IP_ = df_main.loc[last_line, 'last_IP']
        #last_IP_ = df_main['last_IP'].max()
        print(f'''Последний используемый IP: {last_IP_}
Последний используемый заводской номер: {last_ZvN}
''')


        if df_main['last_serial_number'].idxmax() != df_main['last_IP'].idxmax():
            print(f"""Предупреждени! Ошибка вычисления максимального значения: 
            индекс заводского номера - {df_main['last_serial_number'].idxmax()}
            индекс IP - {df_main['last_IP'].idxmax()}
            """)

        last_IP = ipaddress.ip_address(last_IP_)
        new_last_IP = last_IP + stickers_count
        new_last_ZvN = last_ZvN + stickers_count
        new_first_IP = last_IP + 1
        new_first_ZvN = last_ZvN + 1
        print(f'Новый последний IP: {new_last_IP}')


    order_number = last_order_number + 1

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
#end of main function

def IP_range_check(df_base, index): #checks whether the IP address belongs to a valid range
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

def df_preparing (df_main, df_base, equipment_name, equipment_type):
    df = df_main
    equipment_df = df_base
    df_2 = df_filter(df, 'equipment_name', equipment_name)
    equipment_df_2 = df_filter(equipment_df, 'equipment_name', equipment_name)
    df_3 = df_filter(df_2, 'equipment_type', equipment_type)
    equipment_df_3 = df_filter(equipment_df_2, 'equipment_type', equipment_type)
    return df, equipment_df, df_3, equipment_df_3

def save_button (df_main, df_base, equipment_name, equipment_type, stickers_count):

    df, equipment_df, df_3, equipment_df_3 = df_preparing(df_main, df_base, equipment_name, equipment_type)

    equipment_index = equipment_df_3.index #РАЗОБРАТЬСЯ!!!!!!!!!!!!!!
    equipment_df_3 = index_reset(equipment_df_3)

    last_order_number = last_order_number_func (df)

    df_add = {}

    df_add = new_order_creating(df_3, equipment_df_3, stickers_count, last_order_number, equipment_name, equipment_type)
    #LAUNCHING THE MAIN FUNCTION!!!



    equipment_index_int = int(equipment_index[0])
    IP_range_check(equipment_df, equipment_index_int)

    df = df._append(df_add, ignore_index= True)

    df.to_excel("Main_file.xlsx", index=False) #Main file updating with new line/order




