#Это самое начало кода

#s = input('введите s ')
#print(s)

# Import module
import ipaddress

# Arithmetic Operation on IPv4 address
#print(ipaddress.IPv4Address(u'129.117.0.0') - 6)
#print(ipaddress.IPv4Address(u'175.199.42.211') + 55)
#print(ipaddress.IPv4Address(u'255.255.255.255') + 1)
#print(ipaddress.IPv4Address(u'0.0.0.0') - 1)

StN = int(input("Введите стартовый номер: "))
ZvN = int(input("Введите заводской номер: "))

print(f'{StN}, {ZvN}')

#print(ipaddress.IPv4Address(u'10.8.0.0') + (ZvN//256+StN)*256 + ZvN%256)
print(f" {ZvN // 256 + StN}*256, {ZvN % 256}")

