import ipaddress
i = 0
while i < 20:
    try:
        StN = int(input("Введите стартовый номер: "))
    except ValueError: print("введите ЧИСЛО")

    else:
        if StN in range(0, 256):
            try:
                ZvN = int(input("Введите заводской номер: "))
            except ValueError: print("введите ЧИСЛО")

            else:
                IP = ipaddress.IPv4Address(u'10.8.0.0') + (ZvN // 256 + StN) * 256 + ZvN % 256
                if IP >= ipaddress.IPv4Address(u'10.9.0.0') or IP < ipaddress.IPv4Address(u'10.8.0.0'):
                    print ("IP вне диапазона 10.8")
                else:
                    print(f"IP устройства: {IP}")
                    i += 1
        else: print("Стартовый номер должен быть в пределах от 0 до 255")
else: print("Пора отдохнуть")


        # print(f'{StN}, {ZvN}')
        # print(f" {ZvN // 256 + StN}*256, {ZvN % 256}")
