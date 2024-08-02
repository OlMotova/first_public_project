import ipaddress
StN = int(input("Введите стартовый номер: "))
ZvN = int(input("Введите заводской номер: "))
#print(f'{StN}, {ZvN}')
print(f"IP устройства: {ipaddress.IPv4Address(u'10.8.0.0') + (ZvN // 256 + StN) * 256 + ZvN % 256}")
#print(f" {ZvN // 256 + StN}*256, {ZvN % 256}")