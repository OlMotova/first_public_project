import flet as ft
import pandas as pd 
import os
from functions import *

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
        
        if os.path.exists('Main_file.xlsx'):
            self.df = pd.read_excel('Main_file.xlsx')
        # else:
            # ft.alert('Файл Main_file_test.xlsx не найден.')

        if os.path.exists('equipment_database.xlsx'):
            self.equipment_df = pd.read_excel('equipment_database.xlsx')
        # else:
            # ft.alert('Файл equipment_database.xlsx не найден.')


        self.df = pd.read_excel('Main_file.xlsx')
        self.equipment_df = pd.read_excel('equipment_database.xlsx')

        # Изначальные данные
        self.list_equi = self.unique_equipment(self.equipment_df, 'equipment_name')
        dropdown_equi_option = [ft.dropdown.Option(item) for item in self.list_equi]



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
            options=dropdown_equi_option,
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
        self.buttom_count = ft.IconButton(
            tooltip="Подсчет диапазона",
            icon=ft.icons.CALCULATE_OUTLINED,
            icon_size=30,                                          
            style=self.buttom_style,
            on_click=self.calc
        )
        # Кнопка первичного подсчета
        self.buttom_write = ft.IconButton (
            tooltip="Подсчет и запись в файл",
            icon=ft.icons.CHECKLIST,
            icon_size=30,
            style=self.buttom_style,
            on_click=lambda e: self.page.open(self.dlg_modal)
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
        
        # ввод нового оборудования
        self.textfield_name = ft.TextField(
            label='Название',
            label_style=ft.TextStyle(color=ft.colors.WHITE),
            hint_text="Введите название",
            cursor_color=ft.colors.WHITE,
            bgcolor="#5c5a57",
            border_color="#c1c2bf",
            color=ft.colors.WHITE,
            border_width=1,
            border_radius=20
        )
        # ввод нового типа оборудования
        self.textfield_type = ft.TextField(
            label='Тип',
            label_style=ft.TextStyle(color=ft.colors.WHITE),
            hint_text="Введите тип",
            cursor_color=ft.colors.WHITE,
            bgcolor="#5c5a57",
            border_color="#c1c2bf",
            color=ft.colors.WHITE,
            border_width=1,
            border_radius=20
        )
        # ввод начала нового диапазона
        self.textfield_start = ft.TextField(
            label='Начало',
            label_style=ft.TextStyle(color=ft.colors.WHITE),
            hint_text="Введите начальное значение диапазона",
            cursor_color=ft.colors.WHITE,
            bgcolor="#5c5a57",
            border_color="#c1c2bf",
            color=ft.colors.WHITE,
            width=192,
            border_width=1,
            border_radius=20
        )
        
        # ввод конца нового диапазона
        self.textfield_end = ft.TextField(
            label='Конец',
            label_style=ft.TextStyle(color=ft.colors.WHITE),
            hint_text="Введите конечное значение диапазона",
            cursor_color=ft.colors.WHITE,
            bgcolor="#5c5a57",
            border_color="#c1c2bf",
            color=ft.colors.WHITE,
            width=192,
            border_width=1,
            border_radius=20
        )
        # кнопка добавления
        self.buttom_append = ft.ElevatedButton(
            text="Добавить",
            style=self.buttom_style)

        
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
                    self.textfield_name,
                    self.textfield_type,
                    ft.Row(
                        controls=[
                        self.textfield_start,
                        self.textfield_end
                        ]
                    ),
                    ft.Row(
                        controls=[
                            self.buttom_append    
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    )
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
            title=ft.Text("ну и что ты заказывать собрался?"),
            content=ft.Text("--тут будет написан диапазон--"),
            actions=[
                ft.TextButton("я принимаю ответственность", on_click=self.handle_close),
                ft.TextButton("нет я уже смешарик", on_click=self.handle_close),
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

    def handle_close(self,e):
        self.page.close(self.dlg_modal)
            # page.add(ft.Text(f"Modal dialog closed with action: {e.control.text}"))

            
        
        # Функция для открытия BottomSheet
    def show_bottom_sheet(self, e):
        print("BottomSheet: ")
        self.bottom_sheet.open = True  # Открываем BottomSheet
        self.page.update()  # Обновляем страницу


        

        
  

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
        # Обработка выбора типа
        # print(f"Selected type: {selected_value}")
        return selected_value



    def calc(self, e):
        
        self.type = self.dropdown_type.value
        self.equipment = self.dropdown_equp.value
        self.count_stick = int(self.textfield_count.value)

        x,y =calculating_button(self.df,self.equipment_df, self.equipment, self.type, self.count_stick)
        # print(self.type,self.equipment,self.count_stick)
        # print(calculating_button())
        self.listview_info.controls.append(
            ft.Text(
                value=f"({x},{y})",
                color=self.color_text,
                weight=ft.FontWeight.W_600,
                selectable=True
            )
        )
        self.page.update()

        
    
    # def choose_cont(self):

    #     self.info = ft.Container(
    #             content=self.Row,
    #             padding=10,
    #             border=ft.border.all(5, ft.colors.BLUE_400),
    #             border_radius=ft.border_radius.all(40),
    #             height=600,
    #             bgcolor=ft.colors.BLUE_100,
    #             expand=3
    #         )
    #     return self.info   


    # def choose_cont(self):

    #     self.first_row = ft.Row(controls=[self.equipments_dropdown,self.type_dropdown,self.num_field])
    #     self.second_row = ft.Row(alignment=ft.MainAxisAlignment.END,
    #                              controls=[self.buttom_count,self.buttom_write])

    #     self.main_column = ft.Column(alignment=ft.MainAxisAlignment.CENTER,controls=[self.first_row,self.second_row])

    #     self.info = ft.Container(
    #             content=self.main_column,
    #             padding=10,
    #             border=ft.border.all(5, ft.colors.BLUE_400),
    #             border_radius=ft.border_radius.all(40),            
    #             bgcolor=ft.colors.BLUE_100,
    #             expand=True
    #         )
    #     return self.info  

    # def info_cont(self):

         
    #      self.info = ft.Container(
    #             # content=self.main_column,
    #             padding=10,
    #             border=ft.border.all(5, ft.colors.BLUE_400),
    #             border_radius=ft.border_radius.all(40),            
    #             bgcolor=ft.colors.BLUE_100,
    #             expand=True
    #         )
    #      return self.info
    
    # def add_cont(self):
        

    #     self.info = ft.Container(
    #             # content=self.main_column,
    #             padding=10,
    #             border=ft.border.all(5, ft.colors.BLUE_400),
    #             border_radius=ft.border_radius.all(40),            
    #             bgcolor=ft.colors.BLUE_100,
    #             expand=True
    #         )
    #     return self.info 
  

    def run(self):
        self.page.add(
            self.count_main,
            self.bottom_sheet                          
            
        )
        self.page.update

def main(page: ft.Page):

    window = MainWindow(page)
    page.window.height = 600
    page.window.width = 450
    window.run()


if __name__ == '__main__':
    ft.app(target=main, view=ft.AppView.FLET_APP)