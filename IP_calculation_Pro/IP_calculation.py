import pandas as pd

#loading start

url = 'https://docs.google.com/spreadsheets/d/1mPWR7CGOOu268woDhUocSk2owEBvMrNEzFNC2t6ArCU/edit?usp=sharing'

import re

def convert_google_sheet_url(url):
    # Regular expression to match and capture the necessary part of the URL
    pattern = r'https://docs\.google\.com/spreadsheets/d/([a-zA-Z0-9-_]+)(/edit#gid=(\d+)|/edit.*)?'

    # Replace function to construct the new URL for CSV export
    # If gid is present in the URL, it includes it in the export URL, otherwise, it's omitted
    replacement = lambda m: f'https://docs.google.com/spreadsheets/d/{m.group(1)}/export?' + (f'gid={m.group(3)}&' if m.group(3) else '') + 'format=csv'

    # Replace using regex
    new_url = re.sub(pattern, replacement, url)

    return new_url

new_url = convert_google_sheet_url(url)

print(new_url)
# https://docs.google.com/spreadsheets/d/1mSEJtzy5L0nuIMRlY9rYdC5s899Ptu2gdMJcIalr5pg/export?gid=1606352415&format=csv

df = pd.read_csv(new_url)

#loading end

print(df.head())

print('________________________')

print(df.dtypes)

#data type convert
from datetime import datetime
import ipaddress

df['order_date'] = pd.to_datetime(df['order_date'], format='%d.%m.%Y')
#df['last_IP'] = df['last_IP'].ip.apply(lambda x: ipaddress.ip_address(x))


print('________________________')
print(df.dtypes)

print(df.describe())
print('________________________')

print(df['equipment_name'].unique())
equipment_name = input("Введите имя устройства: ")

df_2 = df[df['equipment_name'] == equipment_name]
print(df_2)

print('________________________')
max_IP = df_2['last_IP'].max()
print(f'Последний используемый IP: {max_IP}')
