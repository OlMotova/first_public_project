# -*- coding: utf-8 -*-
import pandas as pd
from functions import *

def check_IP_range_overlap(df_base_IP, first_IP, last_IP):
    # Convert input IP range to IP address objects
    first_IP = ipaddress.IPv4Address(first_IP)
    last_IP = ipaddress.IPv4Address(last_IP)

    # Convert IP ranges to actual IP objects for comparison
    df_base_IP['first_IP'] = df_base_IP['first_IP'].apply(ipaddress.IPv4Address)
    df_base_IP['last_IP'] = df_base_IP['last_IP'].apply(ipaddress.IPv4Address)

    # Check the input range against each row in the data
    for i in range(len(df_base_IP)):
        range_start, range_end = df_base_IP['first_IP'][i], df_base_IP['last_IP'][i]

        # Check if the input range overlaps with any range in the table
        if first_IP <= range_end and range_start <= last_IP:
            return False
    return True

def check_IP_range_overlap_in_file(df_base_IP):
    # Convert IP ranges to actual IP objects for comparison
    df_base_IP['first_IP'] = df_base_IP['first_IP'].apply(ipaddress.IPv4Address)
    df_base_IP['last_IP'] = df_base_IP['last_IP'].apply(ipaddress.IPv4Address)

    n = len(df_base_IP)

    # Check each pair of ranges for overlap
    for i in range(n):
        for j in range(i + 1, n):
            range1_start, range1_end = df_base_IP['first_IP'][i], df_base_IP['last_IP'][i]
            range2_start, range2_end = df_base_IP['first_IP'][j], df_base_IP['last_IP'][j]

            # Check if the ranges overlap
            if range1_start <= range2_end and range2_start <= range1_end:
                print(f"Строка файла equipment_IP_database.xlsx {i+2} пересекается со строкой {j+2}")
                return False

    return True

def check_ip_serial_difference(df_base_IP):
    # Convert IP ranges to actual IP objects for comparison
    df_base_IP['first_IP'] = df_base_IP['first_IP'].apply(ipaddress.IPv4Address)
    df_base_IP['last_IP'] = df_base_IP['last_IP'].apply(ipaddress.IPv4Address)

    # Check the input range against each row in the data
    for i in range(len(df_base_IP)):
        IP_range_start, IP_range_end = df_base_IP['first_IP'][i], df_base_IP['last_IP'][i]
        ZvN_range_start, ZnN_range_end = df_base_IP['first_serial_number'][i], df_base_IP['last_serial_number'][i]

        # Calculate IP range difference
        ip_range_diff = int(IP_range_end) - int(IP_range_start)
        # Calculate serial number range difference
        serial_range_diff = ZnN_range_end - ZvN_range_start

        # Check if the differences are not equal
        if ip_range_diff != serial_range_diff:
            print(f'Ошибка диапазонов в строке {i + 2}')
            return False

    return True

def new_equipment_df_line_creating(equipment_name, equipment_type,  new_first_ZvN, new_last_ZvN, new_first_IP, new_last_IP, ab_label): #Returns df line with new data for adding to eq_base file

    df_add = {
        'equipment_name': equipment_name,
        'equipment_type': equipment_type,
        'first_serial_number': new_first_ZvN,
        'last_serial_number': new_last_ZvN,
        'first_IP': new_first_IP,
        'last_IP': new_last_IP,
        'ab_label': ab_label
    }
    return df_add
def calculating_button_service (df_base_IP, equipment_name, equipment_type, first_ip, last_ip):
    #проверяем базу
    if check_IP_range_overlap_in_file(df_base_IP) == False:
        return False, None, None
    if check_ip_serial_difference(df_base_IP) == False:
        return False, None, None

    #проверяем пересечения диапазонов новых IP с данными в таблице
    if check_IP_range_overlap(df_base_IP, first_ip, last_ip) == False:
        return False, None, None

    equipment_df_1 = df_filter(df_base_IP, 'equipment_name', equipment_name)
    equipment_df_2 = df_filter(equipment_df_1, 'equipment_type', equipment_type)
    #расчет заводских номеров в зависимости от того, новое ли наименование оборудования
    if equipment_df_2.empty:
        first_ZvN = 1
    else:
        first_ZvN = equipment_df_2['last_serial_number'].max() + 1

    first_IP = ipaddress.IPv4Address(first_ip)
    last_IP = ipaddress.IPv4Address(last_ip)

    last_ZvN = first_ZvN + int(last_IP) - int(first_IP)
    #проверка IP на корректность порядка ввода
    if (int(last_IP) - int(first_IP)) < 1:
        return False, None, None

    return True, first_ZvN, last_ZvN

def save_button_service (df_base_types, df_base_IP, equipment_name, equipment_type, equipment_version, first_ZvN, last_ZvN, first_IP, last_IP, new = None):

    ab_label = 'open'

    df_add = new_equipment_df_line_creating(equipment_name, equipment_type, first_ZvN, last_ZvN, first_IP, last_IP, ab_label)

    df = df_base_IP._append(df_add, ignore_index=True)

    try:
        #обновление таблицы с наименованиями
        if new == True:
            df_types_add = {
                'equipment_name': equipment_name,
                'equipment_type': equipment_type,
                'equipment_version': equipment_version
            }

            df_types = df_base_types._append(df_types_add, ignore_index=True)
            df_types.to_excel("equipment_database.xlsx", index=False)  # save new line to file
        #обновление базы IP
        df.to_excel("equipment_IP_database.xlsx", index=False)  # save new line to file

    except PermissionError:
        print("Закройте файл и попробуйте снова!")



        #text = 'Базы обновлены'
        #flag = True
        #return flag

    #text = 'База IP обновлена'
    #flag = True

#    return flag