import pandas as pd
import ipaddress

# Define the subnet
subnet = ipaddress.ip_network('192.168.0.0/24')

# Create a DataFrame with all IP addresses in the subnet
df = pd.DataFrame({'ip_address': list(subnet.hosts())})

print(df.dtypes)

print(df.describe())



#______________________
url = 'https://docs.google.com/spreadsheets/d/1mPWR7CGOOu268woDhUocSk2owEBvMrNEzFNC2t6ArCU/edit?usp=sharing'

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

df = pd.read_csv(new_url)
#__________________________________