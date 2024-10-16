import flet as ft
import pandas as pd 
import os

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
        self.page.bgcolor = ft.colors.BLUE_50  
        
        if os.path.exists('Main_file_test.xlsx'):
            self.df = pd.read_excel('Main_file_test.xlsx')
        # else:
            # ft.alert('Файл Main_file_test.xlsx не найден.')

        if os.path.exists('equipment_database.xlsx'):
            self.equipment_df = pd.read_excel('equipment_database.xlsx')
        # else:
            # ft.alert('Файл equipment_database.xlsx не найден.')


        self.df = pd.read_excel('Main_file_test.xlsx')
        self.equipment_df = pd.read_excel('equipment_database.xlsx')

        # Изначальные данные
        self.list_equi = self.unique_equipment(self.equipment_df, 'equipment_name')
        dropdown_equi_option = [ft.dropdown.Option(item) for item in self.list_equi]

        self.equipments_dropdown = ft.Dropdown(
            label_style=ft.TextStyle(color=ft.colors.WHITE),
        # Добавляем элементы на страницу        
            hint_text="Выберите оборудование",
            hint_style=ft.TextStyle(color=ft.colors.WHITE),
            bgcolor=ft.colors.BLUE_600,
            border_width=5,
            border_radius=30,
            border_color=ft.colors.INDIGO,
            color=ft.colors.WHITE,
            options=dropdown_equi_option,
            expand=True,
            autofocus=True,
            on_change=self.equipments_dropdown_change
        )

        # Изначально пустой dropdown для типа
        self.type_dropdown = ft.Dropdown(
            label_style=ft.TextStyle(color=ft.colors.WHITE),
            hint_text="Выберите тип",
            hint_style=ft.TextStyle(color=ft.colors.WHITE),
            bgcolor=ft.colors.BLUE_600,
            border_width=5,
            border_radius=30,
            border_color=ft.colors.INDIGO,
            color=ft.colors.WHITE,
            options=[],  # Начально пустой
            expand=True,
            autofocus=True,
            on_change=self.type_dropdown_change
        )

        self.num_field = ft.TextField(
                            label='Количество',
                            label_style=ft.TextStyle(color=ft.colors.WHITE),
                            hint_text="Введите количество наклеек",
                            cursor_color=ft.colors.WHITE,
                            bgcolor=ft.colors.BLUE_600,
                            color=ft.colors.WHITE,
                            border_width=5,
                            border_radius=30
        )

        self.buttom_count = ft.IconButton(icon=ft.icons.CALCULATE_OUTLINED,
                                          icon_size=50,                                          
                                                            style=ft.ButtonStyle(
                                                                bgcolor={ft.MaterialState.DEFAULT: ft.colors.BLUE_400,
                                                                        ft.MaterialState.FOCUSED: ft.colors.TEAL_400,
                                                                        ft.MaterialState.HOVERED: ft.colors.BLUE_600
                                                                        },
                                                                color={
                                                                    ft.MaterialState.HOVERED: ft.colors.WHITE,
                                                                    ft.MaterialState.DEFAULT: ft.colors.BLACK,
                                                                    }
            ),
            # on_click=self.click_firmware
        )
        self.buttom_write = ft.IconButton(icon=ft.icons.CHECKLIST,
                                          icon_size=50,
                                                        style=ft.ButtonStyle(
                                                                bgcolor={ft.MaterialState.DEFAULT: ft.colors.BLUE_400,
                                                                        ft.MaterialState.FOCUSED: ft.colors.TEAL_400,
                                                                        ft.MaterialState.HOVERED: ft.colors.BLUE_600
                                                                        },
                                                                color={
                                                                    ft.MaterialState.HOVERED: ft.colors.WHITE,
                                                                    ft.MaterialState.DEFAULT: ft.colors.BLACK,
                                                                    }
            ),
            # on_click=self.click_firmware
        )




    def unique_equipment(self, df, column):
        unique_equipment_list = df[column].unique()
        return unique_equipment_list

    def equipments_dropdown_change(self, e):
        selected_value = self.equipments_dropdown.value

        if selected_value:
            # Фильтрация данных
            self.equipment_df_2 = self.equipment_df[self.equipment_df['equipment_name'] == selected_value]
            self.update_type_dropdown()

    def update_type_dropdown(self):
        # Обновление списка для типа
        self.type_list = self.unique_equipment(self.equipment_df_2, 'equipment_type')
        dropdown_type_option = [ft.dropdown.Option(item) for item in self.type_list]
        self.type_dropdown.options = dropdown_type_option
        self.page.update()

    def type_dropdown_change(self, e):
        selected_value = self.type_dropdown.value
        # Обработка выбора типа
        # print(f"Selected type: {selected_value}")
        return selected_value
    
    def choose_cont(self):

        self.info = ft.Container(
                content=self.Row,
                padding=10,
                border=ft.border.all(5, ft.colors.BLUE_400),
                border_radius=ft.border_radius.all(40),
                height=600,
                bgcolor=ft.colors.BLUE_100,
                expand=3
            )
        return self.info   


    def choose_cont(self):

        self.first_row = ft.Row(controls=[self.equipments_dropdown,self.type_dropdown,self.num_field])
        self.second_row = ft.Row(alignment=ft.MainAxisAlignment.END,
                                 controls=[self.buttom_count,self.buttom_write])

        self.main_column = ft.Column(alignment=ft.MainAxisAlignment.CENTER,controls=[self.first_row,self.second_row])

        self.info = ft.Container(
                content=self.main_column,
                padding=10,
                border=ft.border.all(5, ft.colors.BLUE_400),
                border_radius=ft.border_radius.all(40),            
                bgcolor=ft.colors.BLUE_100,
                expand=True
            )
        return self.info  

    def info_cont(self):

         
         self.info = ft.Container(
                # content=self.main_column,
                padding=10,
                border=ft.border.all(5, ft.colors.BLUE_400),
                border_radius=ft.border_radius.all(40),            
                bgcolor=ft.colors.BLUE_100,
                expand=True
            )
         return self.info
    
    def add_cont(self):
        

        self.info = ft.Container(
                # content=self.main_column,
                padding=10,
                border=ft.border.all(5, ft.colors.BLUE_400),
                border_radius=ft.border_radius.all(40),            
                bgcolor=ft.colors.BLUE_100,
                expand=True
            )
        return self.info 
  

    def run(self):
        self.page.add(
            self.choose_cont(),
            self.info_cont(),
            self.add_cont()
                             
            
        )
        self.page.update

def main(page: ft.Page):

    window = MainWindow(page)
    window.run()


if __name__ == '__main__':
    ft.app(target=main, view=ft.AppView.FLET_APP)