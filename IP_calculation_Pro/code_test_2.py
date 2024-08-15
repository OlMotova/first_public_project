# -*- coding: utf-8 -*-
import pandas as pd
import ipaddress
import re
from datetime import datetime

#loading start

df = pd.read_excel('equipment_database.xlsx')

#loading end

print(df.dtypes)

#def ZvN_calc (index, first_IP, last_IP):
def ZvN_calc (index):
    last_IP = ipaddress.ip_address(df['last_IP'][index])
    first_IP = ipaddress.ip_address(df['first_IP'][index])
    IP_range = int(last_IP) - int(first_IP)
    first_ZvN = df['first_serial_number'][index]
    last_ZvN = int(first_ZvN + IP_range)
    return print(f'{last_ZvN}')

#for i in range(0,12):
#    ZvN_calc(i)

from ipaddress import IPv4Network
first_IP = ipaddress.ip_address(df['first_IP'][11])
last_IP = ipaddress.ip_address(df['last_IP'][11])
print(f'{first_IP}, {last_IP}')

first_net = IPv4Network(first_IP)
last_net = IPv4Network(last_IP)
print(f'{first_net.num_addresses}, {last_net.num_addresses}')

# Вывести префикс можно с помощью свойства prefixlen:net.prefixlen

print(f'{first_net.prefixlen}, {last_net.prefixlen}')

str_first_IP = str(ipaddress.IPv4Address(df['first_IP'][11]))
line_first = str_first_IP.split('.')

str_last_IP = str(ipaddress.IPv4Address(df['last_IP'][11]))
line_last = str_last_IP.split('.')

print(f'''
{line_first[0]} - {line_last[0]} 
{line_first[1]} - {line_last[1]}
{line_first[2]} - {line_last[2]}
{line_first[3]} - {line_last[3]}
''')