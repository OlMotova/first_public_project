import ipaddress
while True:
    try:
        StN = int(input("Введите стартовый номер: "))

        if StN not in range(0, 256):
            print("ОШИБКА: Стартовый номер должен быть в пределах от 0 до 255")
            continue

        else:
            ZvN = int(input("Введите заводской номер: "))
    except ValueError: print("ОШИБКА: введите ЧИСЛО")
    else:

        if ZvN < 0: print("ОШИБКА: номер должен быть больше 0")

        else:
            IP = ipaddress.IPv4Address(u'10.8.0.0') + (ZvN // 256 + StN) * 256 + ZvN % 256
            if IP >= ipaddress.IPv4Address(u'10.9.0.0') or IP < ipaddress.IPv4Address(u'10.8.0.0'):
                print ("ОШИБКА: IP вне диапазона 10.8.")
            else:
                print(f"IP устройства: {IP}")



