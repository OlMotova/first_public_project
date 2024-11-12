# -*- coding: utf-8 -*-
import pandas as pd
import ipaddress
from datetime import datetime
import sys
import numpy as np
from contextlib import redirect_stdout
from functions import *

def new_equipment_df_line_creating(equipment_name, new_first_ZvN, new_last_ZvN, new_first_IP, new_last_IP, ab_label): #Returns df line with new data for adding to eq_base file

    df_add = {
        'equipment_name': equipment_name,
        'first_serial_number': new_first_ZvN,
        'last_serial_number': new_last_ZvN,
        'first_IP': new_first_IP,
        'last_IP': new_last_IP,
        'ab_label': ab_label
    }
    return df_add
def calculating_button_service (df_base, equipment_name, first_ip, last_ip):

    equipment_df_2 = df_filter(df_base, 'equipment_name', equipment_name)

    first_IP = ipaddress.IPv4Address(first_ip)
    last_IP = ipaddress.IPv4Address(last_ip)
    first_ZvN = equipment_df_2['last_serial_number'].max() + 1
    last_ZvN = first_ZvN + int(last_IP) - int(first_IP)

    if (int(last_IP) - int(first_IP)) < 1:
        return False, None, None

    text = 'Данные рассчитаны'
    flag = True
    return flag, first_ZvN, last_ZvN

def save_button_service (df_base_types, df_base_IP, equipment_name, equipment_type, first_ZvN, last_ZvN, first_IP, last_IP, new = None):

    ab_label = 'open'

    df_add = new_equipment_df_line_creating(equipment_name, first_ZvN, last_ZvN, first_IP, last_IP, ab_label)

    df = df_base_IP._append(df_add, ignore_index=True)

    df.to_excel("equipment_IP_database.xlsx", index=False) #save new line to file

    if new == True:
        df_types_add = {
            'equipment_name': equipment_name,
            'equipment_type': equipment_type}

        df_types = df_base_types._append(df_types_add, ignore_index=True)
        df_types.to_excel("equipment_database.xlsx", index=False)  # save new line to file

        #text = 'Базы обновлены'
        flag = True
        #return flag

    #text = 'База IP обновлена'
    flag = True

#    return flag