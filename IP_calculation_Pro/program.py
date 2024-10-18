# -*- coding: utf-8 -*-
from functions import *
import pandas as pd
import ipaddress
from datetime import datetime
import sys
import numpy as np
from contextlib import redirect_stdout

df = df_loading('Main_file.xlsx')
equipment_df = df_loading('equipment_database.xlsx')

print(unique_equipment(equipment_df, 'equipment_name'))
equipment_name = input("Введите (скопируйте) имя устройства: ")

df_2 = df_filter(df, 'equipment_name', equipment_name)
equipment_df_2 = df_filter(equipment_df, 'equipment_name', equipment_name)

print(unique_equipment(equipment_df_2, 'equipment_type'))
equipment_type = input("Введите (скопируйте) тип устройства: ")

df_3 = df_filter(df_2, 'equipment_type', equipment_type)
equipment_df_3 = df_filter(equipment_df_2, 'equipment_type', equipment_type)

stickers_count = int(input("Введите колличество этикеток: "))

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

print("Дальше код не написан")
