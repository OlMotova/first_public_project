# -*- coding: utf-8 -*-
from functions import *
from service_functions import *

df = df_loading('Main_file.xlsx')
equipment_types_df = df_loading('equipment_database.xlsx')
equipment_IP_df = df_loading('equipment_IP_database.xlsx')

print(unique_equipment(equipment_types_df, 'equipment_name'))
equipment_name = input("Введите (скопируйте) имя устройства: ")

df_1 = df_filter(df, 'equipment_name', equipment_name)
equipment_types_df_1 = df_filter(equipment_types_df, 'equipment_name', equipment_name)
equipment_IP_df_1 = df_filter(equipment_IP_df, 'equipment_name', equipment_name)

print(unique_equipment(equipment_types_df_1, 'equipment_type'))
equipment_type = input("Введите (скопируйте) тип устройства: ")

df_2 = df_filter(df_1, 'equipment_type', equipment_type)
equipment_types_df_2 = df_filter(equipment_types_df_1, 'equipment_type', equipment_type)

print(unique_equipment(equipment_types_df_2, 'equipment_version'))
equipment_version = input("Введите (скопируйте) исполнение устройства: ")




stickers_count = int(input("Введите колличество этикеток: "))



#program part

text, flag = calculating_button (df, equipment_IP_df, equipment_name, equipment_type, equipment_version, stickers_count)

text_out = save_button (df, equipment_IP_df, equipment_name, equipment_type, equipment_version, stickers_count)

print(f'''
TEXT: {text}

flag: {flag}

''')

print(text_out)





