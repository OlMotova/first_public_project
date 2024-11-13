import flet as ft
import pandas as pd 
import os
from functions import *
from service_functions import *

class MainWindow:
    def __init__(self, page: ft.Page):

        self.page = page
        self.alert_dialog = None
        self.btn_scan = None
        self.btn_up_all = None
        self.tabs = None
        self.tab_1_class = None
        self.tab_2_class = None
        self.conteiner = None
        self.page.title = 'IW_MD'
        self.page.bgcolor = "#1E1E1E"
        self.color_text = "#c1c2bf"
          

        self.buttom_style_disabled = ft.ButtonStyle(
            bgcolor={
                ft.MaterialState.DEFAULT: "#2c2c2c",
                #  ft.MaterialState.FOCUSED: ft.colors.PINK,
                ft.MaterialState.HOVERED: "#4f4f4f",
            },
            color={
                ft.MaterialState.HOVERED: ft.colors.WHITE,
                ft.MaterialState.DEFAULT: ft.colors.GREY_600,
            },
                )          
        
        self.buttom_style = ft.ButtonStyle(
            bgcolor={
                ft.MaterialState.DEFAULT: "#2c2c2c",
                #  ft.MaterialState.FOCUSED: ft.colors.PINK,
                ft.MaterialState.HOVERED: "#4f4f4f",
            },
            color={
                ft.MaterialState.HOVERED: ft.colors.WHITE,
                ft.MaterialState.DEFAULT: ft.colors.WHITE,
            },
        )
        
        
        # if os.path.exists('Main_file.xlsx'):
        #     self.df = pd.read_excel('Main_file.xlsx')
        # # else:
        #     # ft.alert('Файл Main_file_test.xlsx не найден.')

        # if os.path.exists('equipment_database.xlsx'):
        #     self.equipment_df = pd.read_excel('equipment_database.xlsx')
        # # else:
        #     # ft.alert('Файл equipment_database.xlsx не найден.')


        # self.df = pd.read_excel('Main_file.xlsx')
        # self.equipment_df = pd.read_excel('equipment_database.xlsx')

        # # Изначальные данные
        # self.list_equi = self.unique_equipment(self.equipment_df, 'equipment_name')
        # dropdown_equi_option = [ft.dropdown.Option(item) for item in self.list_equi]

        

        # дропдаун для для названия оборудования
        self.dropdown_equp = ft.Dropdown(
            label_style=ft.TextStyle(color=ft.colors.WHITE),              
            hint_text="Выберите оборудование",
            hint_style=ft.TextStyle(color=ft.colors.WHITE),
            bgcolor="#2c2c2c",
            # border_width=5,
            border_radius=10,
            focused_border_color=ft.colors.TRANSPARENT,
            border_color="#2c2c2c",
            color=ft.colors.WHITE,
            options=[],
            # expand=True,
            autofocus=True,
            on_change=self.equipments_dropdown_change
        )

        # Изначально пустой dropdown для типа
        self.dropdown_type = ft.Dropdown(
            label_style=ft.TextStyle(color=ft.colors.WHITE),
            hint_text="Выберите тип",
            hint_style=ft.TextStyle(color=ft.colors.WHITE),
            bgcolor="#2c2c2c",
            # border_width=5,
            border_radius=10,
            focused_border_color=ft.colors.TRANSPARENT,
            border_color="#2c2c2c",
            color=ft.colors.WHITE,
            options=[],  # Начально пустой
            # expand=True,
            autofocus=True,
            on_change=self.type_dropdown_change
        )
        # количество наклеек
        self.textfield_count = ft.TextField(
            label='Количество',
            label_style=ft.TextStyle(color=ft.colors.WHITE),
            hint_text="Введите количество наклеек",
            cursor_color=ft.colors.WHITE,
            bgcolor="#5c5a57",
            border_color="#c1c2bf",
            color=ft.colors.WHITE,
            
            border_width=1,
            border_radius=20
        )       
        
        # Кнопка подсчета диапазона заказа, пока не нужна
        # self.buttom_count = ft.IconButton(
        #     tooltip="Подсчет диапазона",
        #     icon=ft.icons.CALCULATE_OUTLINED,
        #     icon_size=30,                                          
        #     style=self.buttom_style,
        #     on_click=self.calc
        # )
        # Кнопка первичного подсчета
        self.buttom_write = ft.IconButton (
            tooltip="Подсчет и запись в файл",
            icon=ft.icons.CHECKLIST,
            icon_size=30,
            style=self.buttom_style,
            # on_click=lambda e: self.page.open(self.dlg_modal)
            on_click=self.open_dlg
            )
        # окно вывода информации

        self.listview_info = ft.ListView(expand=True, auto_scroll=True)
        self.count_info = ft.Container(
            content=self.listview_info,
            padding=20,
            # border=ft.border.all(5, '#c1c2bf'),
            border_radius=ft.border_radius.all(20),
            height=300,
            bgcolor="#7a7977"
        )

        # Кнопка появления окна добавления оборудования
        self.buttom_up_window = ft.ElevatedButton(            
            text="Добавить оборудование",
            style=self.buttom_style,
            on_click=self.show_bottom_sheet)
        # self.cont_buttom_up_window = ft.Container(
        #     content=self.buttom_up_window,
        #     padding=10,
        #     alignment=ft.MainAxisAlignment.CENTER
            
        # )

# -----------------------------------------------------------------------------------
        
        self.dropdown_new_equp = ft.Dropdown(
            label_style=ft.TextStyle(color=ft.colors.WHITE),
            hint_text="Выберите оборудование",
            hint_style=ft.TextStyle(color=ft.colors.WHITE),
            bgcolor="#2c2c2c",
            border_radius=10,
            focused_border_color=ft.colors.TRANSPARENT,
            border_color="#2c2c2c",
            color=ft.colors.WHITE,
            # options=dropdown_equi_option + [ft.dropdown.Option("Другой...")],  # Добавляем опцию "Другой"
            options=[],
            on_change=self.equipments_dropdown_new_change
        )

        self.dropdown_new_type = ft.Dropdown(
            label_style=ft.TextStyle(color=ft.colors.WHITE),
            hint_text="Выберите тип",
            hint_style=ft.TextStyle(color=ft.colors.WHITE),
            bgcolor="#2c2c2c",
            # border_width=5,
            border_radius=10,
            focused_border_color=ft.colors.TRANSPARENT,
            border_color="#2c2c2c",
            color=ft.colors.WHITE,
            options=[],  # Начально пустой
            # expand=True,
            autofocus=True,
            on_change=self.type_dropdown_new_change
        )

        # ввод нового оборудования
        self.textfield_custom_name = ft.TextField(
            visible=False,
            label='новое оборудование',
            label_style=ft.TextStyle(color=ft.colors.WHITE),
            hint_text="Введите название",
            cursor_color=ft.colors.WHITE,
            bgcolor="#5c5a57",
            border_color="#c1c2bf",
            color=ft.colors.WHITE,
            border_width=1,
            border_radius=20,
            on_change=self.check_input
            # self.custom_input_change # обработчик пользовательского ввода
        )
        # ввод нового типа оборудования
        self.textfield_custom_type = ft.TextField(
            visible=False,
            label='Тип',
            label_style=ft.TextStyle(color=ft.colors.WHITE),
            hint_text="Введите тип",
            cursor_color=ft.colors.WHITE,
            bgcolor="#5c5a57",
            border_color="#c1c2bf",
            color=ft.colors.WHITE,
            border_width=1,
            border_radius=20,
            on_change=self.check_input
            
        )
        # ввод начала нового диапазона
        self.textfield_start = ft.TextField(
            # visible=False,
            disabled=True,
            label='Начало',
            label_style=ft.TextStyle(color=ft.colors.GREY_400),
            hint_text="Введите начальное значение диапазона",
            cursor_color=ft.colors.WHITE,
            bgcolor= "#383838",
            border_color="#c1c2bf",
            color=ft.colors.WHITE,
            width=192,
            border_width=1,
            border_radius=20,
            on_change=self.check_input
        )
        
        # ввод конца нового диапазона
        self.textfield_end = ft.TextField(
            # visible=False,
            disabled=True,
            label='Конец',
            label_style=ft.TextStyle(color=ft.colors.GREY_400),
            hint_text="Введите конечное значение диапазона",
            cursor_color=ft.colors.WHITE,
            bgcolor="#383838",
            border_color="#c1c2bf",
            color=ft.colors.WHITE,
            width=192,
            border_width=1,
            border_radius=20,
            on_change=self.check_input
        )
        # кнопка добавления
        self.buttom_append = ft.ElevatedButton(
            text="Добавить",
            style=self.buttom_style_disabled,
            disabled = True,
            on_click=self.open_dlg_app            
        )
        
        self.cont_buttom_append = ft.Container(
            content=ft.Row(controls=[self.buttom_append],alignment=ft.MainAxisAlignment.CENTER),
            padding=10           
        )
            

        
        # окно вывода информации о записи
        self.count_info_check = ft.Container(
            content=ft.ListView(expand=True, auto_scroll=True),
            padding=20,
            # border=ft.border.all(5, '#c1c2bf'),
            border_radius=ft.border_radius.all(20),
            height=10,
            bgcolor="#7a7977"
        )


        # Контейнер для BottomSheet
        self.cont_up_window = ft.Container(
            content=ft.Column(
                [
                    self.dropdown_new_equp,
                    self.textfield_custom_name,
                    self.dropdown_new_type,
                    self.textfield_custom_type,      
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                        self.textfield_start,
                        self.textfield_end
                        ]
                    ),
                    self.cont_buttom_append
                    # ft.Row(
                    #     controls=[
                    #         self.buttom_append    
                    #     ],
                    #     alignment=ft.MainAxisAlignment.CENTER
                    # )
                ]
            ),
            padding=20,
            # border=ft.border.all(5, '#c1c2bf'),
            border_radius=ft.border_radius.all(20),
            height=500,
            bgcolor="#1E1E1E"
        )
        # Определяем BottomSheet
        self.bottom_sheet = ft.BottomSheet(
            content=self.cont_up_window,
            open=False  # Начально закрыт
        )

        # ---------------------------------------------------
        self.dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("ну и что заказывать будем?"),
            # content=ft.Text(f"--тут будет написан диапазон--"),
            actions=[
                ft.TextButton("пойдет", on_click=self.calc),
                ft.TextButton("нет я уже смешарик", on_click=self.handle_close),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            on_dismiss=lambda e: page.add(
                ft.Text("Modal dialog dismissed"),
            ),
        )
        self.dlg_err = ft.AlertDialog(
            modal=True,
            title=ft.Text("Ошибка"),
            # content=ft.Text(f"--тут будет написан диапазон--"),
            actions=[
                # ft.TextButton("пойдет", on_click=self.calc),
                ft.TextButton("Какая то ошибка", on_click=self.err_close),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            on_dismiss=lambda e: page.add(
                ft.Text("Modal dialog dismissed"),
            ),
        )
        self.dlg_app = ft.AlertDialog(
            modal=True,
            title=ft.Text("Добавляем?"),
            # content=ft.Text(f"--тут будет написан диапазон--"),
            actions=[
                ft.TextButton("Действуй решительно", on_click=self.save_equp),
                ft.TextButton("Нет, я передумал", on_click=self.app_close),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            on_dismiss=lambda e: page.add(
                ft.Text("Modal dialog dismissed"),
            ),
        )            


        self.count_main = ft.Container(            
            content=ft.Column(                
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    self.dropdown_equp,
                    self.dropdown_type,
                    ft.Row(
                        controls=[
                            self.textfield_count,
                            # self.buttom_count,
                            self.buttom_write
                        ],
                        alignment=ft.MainAxisAlignment.CENTER                    
                    ),
                    self.count_info,
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[self.buttom_up_window])              
                ]
            )
        )

    def update_file(self):
        # Загружаем файлы через метод load_file
        self.df = self.load_file('Main_file.xlsx')
        self.equipment_df = self.load_file('equipment_database.xlsx')
        self.equipment_IP_df = self.load_file('equipment_IP_database.xlsx')

        # Изначальные данные для оборудования
        self.list_equi = self.unique_equipment(self.equipment_df, 'equipment_name')
        dropdown_equi_option_main = [ft.dropdown.Option(item) for item in self.list_equi]
        dropdown_equi_option_bottom = dropdown_equi_option_main + [ft.dropdown.Option("Другой...")]

        # Обновить Dropdown опции
        self.dropdown_equp.options = dropdown_equi_option_main
        self.dropdown_equp.update()  # Обновить отображение Dropdown

        self.dropdown_new_equp.options = dropdown_equi_option_bottom
        self.dropdown_new_equp.update
#
        
        
    def load_file(self, file_name: str) -> pd.DataFrame:
        """Проверяет наличие файла и загружает его в DataFrame."""
        if os.path.exists(file_name):
            
            """Добавить функцию проверки!!!!!!!!!!!!!"""
            
            return pd.read_excel(file_name)
        else:
            print(f"Файл {file_name} не найден.")
            return pd.DataFrame()  # Возвращаем пустой DataFrame если файл не найден

    def handle_close(self,e):
        self.page.close(self.dlg_modal)
            # page.add(ft.Text(f"Modal dialog closed with action: {e.control.text}"))

    def err_close(self,e):
        self.page.close(self.dlg_err)

    def app_close(self,e):
        self.page.close(self.dlg_app)

            
        
        # Функция для открытия BottomSheet
    def show_bottom_sheet(self, e):
        print("BottomSheet: ")
        self.bottom_sheet.open = True  # Открываем BottomSheet
        self.page.update()  # Обновляем страницу

    def open_dlg(self, e):
        try:
            self.type = self.dropdown_type.value
            self.equipment = self.dropdown_equp.value
            self.count_stick = int(self.textfield_count.value)


            self.text,self.index =calculating_button(self.df,self.equipment_IP_df, self.equipment, self.type, self.count_stick)
            if self.index == True: 
                self.dlg_modal.content = ft.Text(f"{self.text}")        
                self.page.open(self.dlg_modal)
                # self.dlg_modal.open = True
                self.page.update()
            else:
                self.listview_info.controls.append(ft.Text("---какая то ошибка подсчета---"))     
       
        except ValueError:
            self.listview_info.controls.append(ft.Text("выберите оборудование и количество этикеток"))
            self.page.update()
    def open_dlg_app(self, e):
        try:
            self.append_equipment(e)

            self.index, self.start_zvn, self.end_zvn =calculating_button_service(self.equipment_IP_df, self.app_equp, self.app_start_ip, self.app_end_ip)
            if self.index == True: 
                self.dlg_app.content = ft.Text(f"Будет добавлено {self.app_equp} {self.app_type}\n{self.start_zvn} - {self.app_start_ip} --- {self.end_zvn} - {self.app_end_ip}")
                self.page.open(self.dlg_app)
                # self.dlg_modal.open = True
                self.page.update()
            else:
                self.dlg_err.content = ft.Text(f"{self.app_start_ip} -  {self.app_end_ip}\n ты похоже перепутал")
                # self.listview_info.controls.append(ft.Text("---какая то ошибка подсчета---"))
                self.page.open(self.dlg_err)
                self.page.update()


       
        except ValueError:
            self.dlg_err.content = ft.Text(f"{self.app_start_ip} -  {self.app_end_ip}\n ты похоже перепутал")
            self.page.open(self.dlg_err)
            self.page.update()
  

    def unique_equipment(self, df, column):
        unique_equipment_list = df[column].unique()
        return unique_equipment_list

    def equipments_dropdown_change(self, e):
        selected_value = self.dropdown_equp.value

        if selected_value:
            # Фильтрация данных
            self.equipment_df_2 = self.equipment_df[self.equipment_df['equipment_name'] == selected_value]
            self.update_type_dropdown()


    def update_type_dropdown(self):
        # Обновление списка для типа
        self.type_list = self.unique_equipment(self.equipment_df_2, 'equipment_type')
        dropdown_type_option = [ft.dropdown.Option(item) for item in self.type_list]
        self.dropdown_type.options = dropdown_type_option
        self.page.update()

    def type_dropdown_change(self, e):
        selected_value = self.dropdown_type.value
        # if selected_value == "Другой...":
        # Обработка выбора типа
        print(f"Selected type: {selected_value}")
        return selected_value


        
    def equipments_dropdown_new_change(self, e):
        selected_value = self.dropdown_new_equp.value

        print(f"Selected value_______: {selected_value}")  # Для отладки

        if selected_value == "Другой...":
            # Показываем текстовое поле для ввода пользовательского значения
            self.dropdown_new_type.visible = False
            self.buttom_append.disabled = True
            self.buttom_append.style = self.buttom_style_disabled
            self.textfield_custom_name.visible = True 
            self.textfield_custom_type.visible = True
            self.textfield_start.disabled = False
            self.textfield_end.disabled = False
            self.textfield_start.bgcolor = "#5c5a57"
            self.textfield_start.label_style = ft.TextStyle(color=ft.colors.WHITE)            
            self.textfield_end.label_style = ft.TextStyle(color=ft.colors.WHITE)
            self.textfield_end.bgcolor = "#5c5a57"            
            self.page.update()         
        else:
            self.textfield_start.disabled = True
            self.buttom_append.style = self.buttom_style_disabled
            self.buttom_append.disabled = True
            self.dropdown_new_type.visible = True
            self.textfield_end.disabled = True
            self.textfield_start.value = ""
            self.textfield_start.bgcolor ="#383838"
            self.textfield_start.label_style = ft.TextStyle(color=ft.colors.GREY_400)
            self.textfield_end.value = ""
            self.textfield_end.label_style = ft.TextStyle(color=ft.colors.GREY_400)
            self.textfield_end.bgcolor = "#383838"
            # Если выбран пункт из списка, скрываем текстовое поле
            self.textfield_custom_name.visible = False
            self.textfield_custom_type.visible = False
            # Фильтрация данных
            self.equipment_df_2 = self.equipment_df[self.equipment_df['equipment_name'] == selected_value]
            
            self.update_type_dropdown_new()

    def update_type_dropdown_new(self):
        # Обновление списка для типа
        self.type_list = self.unique_equipment(self.equipment_df_2, 'equipment_type')
        dropdown_new_type_option = [ft.dropdown.Option(item) for item in self.type_list]
        self.dropdown_new_type.options = dropdown_new_type_option + [ft.dropdown.Option("Другой...")]
        self.page.update()

    def type_dropdown_new_change(self, e):
        selected_value = self.dropdown_new_type.value
        if selected_value == "Другой...":
            self.textfield_custom_type.visible = True
            self.buttom_append.disabled = True
            self.buttom_append.style = self.buttom_style_disabled
            self.textfield_start.disabled = False
            self.textfield_end.disabled = False
            self.textfield_start.bgcolor = "#5c5a57"
            self.textfield_start.label_style = ft.TextStyle(color=ft.colors.WHITE)            
            self.textfield_end.label_style = ft.TextStyle(color=ft.colors.WHITE)
            self.textfield_end.bgcolor = "#5c5a57"            
            self.page.update()         
        else:
            self.textfield_start.disabled = True
            self.buttom_append.style = self.buttom_style_disabled
            self.buttom_append.disabled = True
            self.dropdown_new_type.visible = True
            # self.textfield_end.disabled = True
            self.textfield_start.disabled = False
            self.textfield_end.disabled = False
            self.textfield_start.value = ""
            self.textfield_start.bgcolor ="#5c5a57"
            self.textfield_start.label_style = ft.TextStyle(color=ft.colors.WHITE)
            self.textfield_end.value = ""
            self.textfield_end.label_style = ft.TextStyle(color=ft.colors.WHITE)
            self.textfield_end.bgcolor ="#5c5a57"
            # Если выбран пункт из списка, скрываем текстовое поле
            self.textfield_custom_name.visible = False
            self.textfield_custom_type.visible = False
            self.buttom_append.update()
            self.page.update()
            
        # Обработка выбора типа
            print(f"Selected type: {selected_value}")
        return selected_value

    def is_valid_ip(self, ip):
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            return False

    def update_buttom_append_disabled(self, x, style=None):
        self.buttom_append.disabled = x
        self.buttom_append.style = style
        self.buttom_append.update()
        self.page.update()
    
    def check_input(self, e):
        # Проверка на введенный айпишник
        
        ip1_valid = self.is_valid_ip(self.textfield_start.value)
        ip2_valid = self.is_valid_ip(self.textfield_end.value)

        # Enable the button only if both IP addresses are valid
        # self.buttom_append.disabled = not (ip1_valid and ip2_valid)
        if ip1_valid and ip2_valid:
            if self.dropdown_new_equp.value == "Другой...":    
                if len(self.textfield_custom_name.value) > 0 and len(self.textfield_custom_type.value) > 0:     
                    self.update_buttom_append_disabled(False, style=self.buttom_style)
                else:
                    self.update_buttom_append_disabled(True, style=self.buttom_style_disabled)
                    
            elif self.dropdown_new_type.value == "Другой...":
                if len(self.textfield_custom_type.value) > 0:
                    self.update_buttom_append_disabled(False, style=self.buttom_style)                    
                else:
                    self.update_buttom_append_disabled(True, style=self.buttom_style_disabled)
            else:
                self.update_buttom_append_disabled(False, style=self.buttom_style)
        else:
            self.update_buttom_append_disabled(True, style=self.buttom_style_disabled)
        self.buttom_append.update()
        self.page.update()

    def append_equipment(self, e):
        # Добавление нового оборудования
        if self.dropdown_new_equp.value == "Другой...":
            self.app_equp = self.textfield_custom_name.value
            self.app_type = self.textfield_custom_type.value
            self.flag = True
        elif self.dropdown_new_type.value == "Другой...":
                self.app_equp = self.dropdown_new_equp.value
                self.app_type = self.textfield_custom_type.value
                self.app_type = self.textfield_custom_type.value
                self.flag = True
        else:
            self.app_equp = self.dropdown_new_equp.value
            self.app_type = self.dropdown_new_type.value
            self.flag = False

        self.app_start_ip = self.textfield_start.value
        self.app_end_ip = self.textfield_end.value
        

    def save_equp(self,e):
        # Сохранение оборудования        
        save_button_service(self.equipment_df, self.equipment_IP_df,self.app_equp,self.app_type,self.start_zvn,self.end_zvn,self.app_start_ip,self.app_end_ip, self.flag)
        self.app_close(e)

            
    


    def custom_input_change(self, e):
    # Получаем значение из текстового поля
        self.custom_value = self.textfield_custom_name.value

        if self.custom_value:
            # Обновляем данные с пользовательским вводом
            self.equipment_df_2 = self.equipment_df[self.equipment_df['equipment_name'] == self.custom_value]
            self.update_type_dropdown()

        self.page.update()



    def calc(self, e):
        
        self.type = self.dropdown_type.value
        self.equipment = self.dropdown_equp.value
        self.count_stick = int(self.textfield_count.value)

        self.letter = save_button(self.df,self.equipment_IP_df, self.equipment, self.type, self.count_stick)
        # print(self.type,self.equipment,self.count_stick)
        # print(calculating_button())
        self.listview_info.controls.append(
            ft.Text(
                value=f"{self.letter}",
                color=self.color_text,
                weight=ft.FontWeight.W_600,
                selectable=True
            )
        )
        self.handle_close(e)
        self.page.update()
       
    
#    def append_to_list(self, e):
#        if self.dropdown_new_equp.value == "Другой...":
  

    def run(self):
        self.page.add(
            self.count_main)
        self.update_file()
        self.page.add(
             self.bottom_sheet                      
        )
        self.page.update()

def main(page: ft.Page):

    window = MainWindow(page)
    page.window.height = 600
    page.window.width = 550
    window.run()


if __name__ == '__main__':
    ft.app(target=main, view=ft.AppView.FLET_APP)