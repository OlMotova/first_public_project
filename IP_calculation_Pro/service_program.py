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

new =bool(input("Если устройство новое, то введите True: "))


first_IP = input("Введите начальный IP нового диапазона:")
last_IP = input("Введите конечный IP нового диапазона:")


#______________________________________


"""Тестируем сервисную часть"""
#service part

service_flag, first_ZvN, last_ZvN =  calculating_button_service (equipment_IP_df, equipment_name, equipment_type, first_IP, last_IP)

save_button_service (equipment_types_df, equipment_IP_df, equipment_name, equipment_type, equipment_version, first_ZvN, last_ZvN, first_IP, last_IP, new)
# +1 parameter at the end: True if new equipment

print("УСПЕХ!!!")


