# -*- coding: utf-8 -*-
import sys

import pandas as pd
import ipaddress
import numpy as np
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


def IP_converter(IP):
    str_IP = str(IP)
    line_IP = str_IP.split('.')
    return line_IP

#line_first = IP_converter(ipaddress.IPv4Address(df['first_IP'][11]))
#line_last = IP_converter(ipaddress.IPv4Address(df['last_IP'][11]))

first_IP_parts = IP_converter(ipaddress.IPv4Address(df['first_IP'][0]))
last_IP_parts = IP_converter(ipaddress.IPv4Address(df['last_IP'][0]))

print(f'{first_IP_parts[0:3]}, {last_IP_parts[0:3]}')

arrays_equal = np.array_equal(first_IP_parts[0:3], last_IP_parts[0:3])
print((arrays_equal))

if arrays_equal == True:
    print("Проверка пройдена: IP в одном диапазоне")
else:
    print("надо поработать над разделением диапазонов")

#print("Свобода")

#str_first_IP = str(ipaddress.IPv4Address(df['first_IP'][11]))
#line_first = str_first_IP.split('.')

#str_last_IP = str(ipaddress.IPv4Address(df['last_IP'][11]))
#line_last = str_last_IP.split('.')

#print(f'''
#{line_first[0]} - {line_last[0]}
#{line_first[1]} - {line_last[1]}
#{line_first[2]} - {line_last[2]}
#{line_first[3]} - {line_last[3]}
#''')

def createList(r1, r2):
    return list(ip_range(r1, r2 + 1))


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


# Driver Code
r1 = ipaddress.ip_address('10.8.10.0')
r2 = ipaddress.ip_address('10.8.10.5')
list_1 = create_IP_list(r1, r2)
print(list_1)
print(len(list_1))




#list = iprange(r1,r2)

print(list)

def middle_IP_creating(a, b, c):
    middle_IP= ipaddress.ip_address(str(a) + '.' + str(b) + '.' + str(c) + '.' + '255')

    return middle_IP

print(middle_IP_creating(10, 8,30))
print(middle_IP_creating(10, 8,30)+1)