import pandas as pd
from contextlib import redirect_stdout
import ipaddress

# Load the Excel file to check its contents and understand the structure
#file_path = 'equipment_database.xlsx'
file_path = 'Main_file.xlsx'
xls = pd.ExcelFile(file_path)

# Check sheet names and preview the content of the first sheet
sheet_names = xls.sheet_names
sheet_names, pd.read_excel(xls, sheet_name=sheet_names[0]).head()

# Load the data
df = pd.read_excel(xls, sheet_name=sheet_names[0])

# # Function to compare IP and serial ranges
# def check_range_difference(row):
#     # Convert IP addresses to networks
#     first_ip = ipaddress.IPv4Address(row['first_IP'])
#     last_ip = ipaddress.IPv4Address(row['last_IP'])
#
#     # Check if the range of IPs and serial numbers is consistent
#     ip_range_valid = first_ip <= last_ip
#     serial_range_valid = row['first_serial_number'] <= row['last_serial_number']
#
#     return not (ip_range_valid and serial_range_valid)
#
#
# # Apply the function to each row and filter rows where ranges differ
# different_ranges = df[df.apply(check_range_difference, axis=1)]
#
# different_ranges

# Function to calculate the range difference between IP addresses
def calculate_ip_range_difference(row):
    first_ip = ipaddress.IPv4Address(row['first_IP'])
    last_ip = ipaddress.IPv4Address(row['last_IP'])
    # Calculate the difference in the number of IP addresses
    ip_range_diff = int(last_ip) - int(first_ip)
    return ip_range_diff

# Add a new column with the calculated IP range difference
df['ip_range_difference'] = df.apply(calculate_ip_range_difference, axis=1)
df[['equipment_name', 'first_IP', 'last_IP', 'ip_range_difference']].head()


# Function to compare IP and serial number ranges
def check_ip_serial_difference(row):
    # Calculate IP range difference
    ip_range_diff = row['ip_range_difference']
    # Calculate serial number range difference
    serial_range_diff = row['last_serial_number'] - row['first_serial_number']

    # Check if the differences are not equal
    if ip_range_diff != serial_range_diff:
        return f"Warning: [{row.name}] {int(row.name) + 2}  - IP: {ip_range_diff}, Serial: {serial_range_diff}"

    else:
        return "без ошибок"
    return None


# Apply the function to each row and get warnings
warnings = df.apply(check_ip_serial_difference, axis=1)

# Filter and display non-null warnings
warnings.dropna().tolist()


with open('warnings.txt', 'w') as f, redirect_stdout(f):
    print(warnings)

print(warnings)