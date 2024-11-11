# -*- coding: utf-8 -*-
import pandas as pd
import ipaddress
import numpy as np


def df_loading(file_name):
    try:
        return pd.read_excel(file_name)
    except FileNotFoundError:
        print(f"Ошибка: файл {file_name} не найден.")
        return pd.DataFrame()


def df_filter(df, column, value):
    """Фильтрация DataFrame по указанному столбцу и значению."""
    return df[df[column] == value].reset_index(drop=True)


def unique_equipment(df, column):
    """Получение уникальных значений оборудования из DataFrame."""
    return df[column].unique()


def IP_converter(IP):
    """Преобразование IP-адреса в список его сегментов."""
    return str(IP).split('.')


def create_IP_list(start_ip, end_ip):
    """Создание списка IP-адресов между начальным и конечным значением."""
    if start_ip == end_ip:
        return [start_ip]
    else:
        return list(ipaddress.summarize_address_range(ipaddress.ip_address(start_ip), ipaddress.ip_address(end_ip)))


def IP_subtraction(IP_1, IP_2):
    """Вычисление разницы между двумя IP-адресами."""
    IP_1_parts = IP_converter(IP_1)
    IP_2_parts = IP_converter(IP_2)

    if IP_1_parts[:2] == IP_2_parts[:2]:
        difference = (int(IP_2_parts[2]) - int(IP_1_parts[2])) * 256 + (int(IP_2_parts[3]) - int(IP_1_parts[3]))
        return difference
    else:
        return "Слишком большая разница между IP-адресами."


def new_values_calculating(df_main, df_base, stickers_count):
    """Расчет новых значений для нового оборудования или обновления."""
    if df_main.empty:
        try:
            new_first_IP = df_base['first_IP'].max()
            new_last_IP = str(ipaddress.ip_address(new_first_IP) + stickers_count - 1)
            new_first_ZvN = df_base['ZvN'].max() + 1
            new_last_ZvN = new_first_ZvN + stickers_count - 1
            return new_first_ZvN, new_last_ZvN, new_first_IP, new_last_IP, 'open'
        except Exception as e:
            print(f"Ошибка при вычислении новых значений: {e}")
            return None
    else:
        print("Необходимо добавить обработку для обновления существующих данных.")
        return None


def save_button(df, equipment_df, equipment_name, equipment_type, stickers_count):
    """Сохранение данных в файлы."""
    try:
        new_values = new_values_calculating(df, equipment_df, stickers_count)
        if new_values:
            new_first_ZvN, new_last_ZvN, new_first_IP, new_last_IP, ab_label = new_values

            # Добавление новой строки в DataFrame
            df_add = {
                'equipment_name': equipment_name,
                'equipment_type': equipment_type,
                'first_ZvN': new_first_ZvN,
                'last_ZvN': new_last_ZvN,
                'first_IP': new_first_IP,
                'last_IP': new_last_IP,
                'stickers_count': stickers_count,
                'ab_label': ab_label
            }
            df = df.append(df_add, ignore_index=True)
            df.to_excel("Main_file.xlsx", index=False)
            equipment_df.to_excel("equipment_database.xlsx", index=False)
            return f"Данные успешно сохранены для {equipment_name} - {equipment_type}."
        else:
            return "Ошибка при вычислении новых значений."
    except Exception as e:
        return f"Ошибка при сохранении данных: {e}"


def calculating_button(df, equipment_df, equipment_name, equipment_type, stickers_count):
    """Функция для выполнения расчетов и вывода результатов."""
    try:
        df_filtered = df_filter(df, 'equipment_name', equipment_name)
        equipment_filtered = df_filter(equipment_df, 'equipment_type', equipment_type)

        if df_filtered.empty or equipment_filtered.empty:
            return "Оборудование не найдено.", False

        new_values = new_values_calculating(df_filtered, equipment_filtered, stickers_count)
        if new_values:
            return f"Вычисленные значения: {new_values}", True
        else:
            return "Ошибка при вычислении значений.", False
    except Exception as e:
        return f"Ошибка выполнения функции: {e}", False
