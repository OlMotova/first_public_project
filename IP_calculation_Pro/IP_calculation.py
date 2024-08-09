import pandas as pd

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

print(df)

print('________________________')

#df_2 = df[df['switch_last_serial_number'] == ''] yt hf,jnftn
#df_2 = pd.isna(df['switch_last_serial_number'])
#df_3 = df['switch_last_serial_number']
#print(df_2)

j = 0
while pd.notnull(df.at[j, 'switch_last_serial_number']):
    a = df.at[j, 'switch_last_serial_number']
    print(a)
    j += 1
else: print(f"Индекс последней ненулевой строки: {j - 1}")

# i = 0
# while pd.notnull(df.at[i, 'camera_control_unit_last_IP']):
#     i += 1
# else: print(f"Индекс последней ненулевой строки: {i-1}")

#else: print(f'Hi! {i}')