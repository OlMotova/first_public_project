# -*- coding: utf-8 -*-
from functions import *
from service_functions import *
import pandas as pd
import ipaddress
from datetime import datetime
import sys
import numpy as np
from contextlib import redirect_stdout

df = df_loading('Main_file.xlsx')
equipment_types_df = df_loading('equipment_database.xlsx')
equipment_IP_df = df_loading('equipment_IP_database.xlsx')

print(unique_equipment(equipment_types_df, 'equipment_name'))
equipment_name = input("Введите (скопируйте) имя устройства: ")

df_2 = df_filter(df, 'equipment_name', equipment_name)
equipment_df_2 = df_filter(equipment_types_df, 'equipment_name', equipment_name)
#equipment_IP_df_2 = df_filter(equipment_IP_df, 'equipment_name', equipment_name)

print(unique_equipment(equipment_df_2, 'equipment_type'))
equipment_type = input("Введите (скопируйте) тип устройства: ")


#stickers_count = int(input("Введите колличество этикеток: "))

first_IP = input("Введите начальный IP нового диапазона:")
last_IP = input("Введите конечный IP нового диапазона:")


#______________________________________
# """Заблочена расчетная расть программы"""
#program part

# text, flag = calculating_button (df, equipment_IP_df, equipment_name, equipment_type, stickers_count)
#
# text_out = save_button (df, equipment_IP_df, equipment_name, equipment_type, stickers_count)
#
# print(f'''
# TEXT: {text}
#
# flag: {flag}
#
# ''')
#
# print(text_out)

"""Тестируем сервисную часть"""
#service part

service_text, service_flag, first_ZvN, last_ZvN =  calculating_button_service (equipment_IP_df, equipment_name, first_IP, last_IP)

service_text_s, service_flag_s = save_button_service (equipment_types_df, equipment_IP_df, equipment_name, equipment_type, first_ZvN, last_ZvN, first_IP, last_IP)
# +1 parameter at the end: True if new equipment

print(service_text)

print(service_text_s)
