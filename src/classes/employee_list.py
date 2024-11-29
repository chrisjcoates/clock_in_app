from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.screenmanager import Screen
from kivy.graphics import Rectangle, Color
from classes.database import Database


class EmployeeListWindow(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.database = Database()

        self.main_layout = BoxLayout(
            orientation="vertical", spacing=0, padding=0)
        self.square_background(self.main_layout, (1, 1, 1, 1))
        self.main_layout.bind(size=self.layout_bg, pos=self.layout_bg)

        self.second_layout = BoxLayout(
            orientation="vertical", padding=0, spacing=0)

        self.second_layout.add_widget(self.create_button_container())
        self.second_layout.add_widget(self.create_table_container("all"))
        self.main_layout.add_widget(self.create_nav())
        self.main_layout.add_widget(self.second_layout)

        self.all_button.bind(
            on_press=lambda instance: self.update_table("all"))
        self.clocked_in_button.bind(
            on_press=lambda instance: self.update_table("clocked in")
        )
        self.clocked_out_button.bind(
            on_press=lambda instance: self.update_table("clocked out")
        )

        self.bind(on_enter=lambda instance: self.update_table("all"))

        self.add_widget(self.main_layout)

    def reset_nav(self, instance, text):
        self.nav_spinner.text = "Menu"

    def switch_screen(self, instance, text):

        original_text = text

        if original_text == "Add Employee":
            self.manager.current = "add_employees"
        elif original_text == "Clock-in/out":
            self.manager.current = "main_window"

        self.reset_nav(instance, text)

    def create_nav(self):
        container = BoxLayout(orientation="vertical")
        self.square_background(container, (0.129, 0.129, 0.129, 1))
        container.bind(size=self.layout_bg, pos=self.layout_bg)
        container.size_hint = (1, None)
        container.height = 100

        self.nav_spinner = Spinner(
            text="Menu", values=["Clock-in/out", "Add Employee"])
        self.nav_spinner.bind(text=self.switch_screen)
        container.add_widget(self.nav_spinner)

        return container

    def create_button_container(self):
        container = BoxLayout(orientation="horizontal", padding=10)
        self.square_background(container, (0.129, 0.129, 0.129, 1))
        container.bind(size=self.layout_bg, pos=self.layout_bg)
        container.size_hint = (1, None)
        container.height = 100
        self.all_button = Button(text="All")
        self.clocked_in_button = Button(text="Clocked-in")
        self.clocked_out_button = Button(text="Clocked-out")

        container.add_widget(self.all_button)
        container.add_widget(self.clocked_in_button)
        container.add_widget(self.clocked_out_button)

        return container

    def create_table_container(self, filter=None):

        self.table = ScrollView(size_hint=(1, 1))

        container = BoxLayout(
            orientation="vertical", size_hint_y=None, spacing=10, padding=10
        )
        container.bind(minimum_height=container.setter("height"))

        header_layout = BoxLayout(orientation="horizontal")
        self.square_background(header_layout, (0.7, 0.7, 0.7, 0.7))
        header_layout.bind(size=self.layout_bg, pos=self.layout_bg)
        header_layout.size_hint = (1, None)
        header_layout.height = 80
        container.add_widget(header_layout)

        headers = [
            "First Name",
            "Last Name",
            "Location",
            "Clocked-in",
            "Timestamp",
        ]

        id_label = Label(text='ID', size_hint=(None, 1), width=100)
        id_label.color = (0, 0, 0, 1)
        header_layout.add_widget(id_label)

        for header in headers:
            label = Label(text=header, size_hint=(1, None))
            label.color = (0, 0, 0, 1)
            header_layout.add_widget(label)

        employees = self.database.get_all_records(filter)

        label_list = []

        for employee in employees:
            emp_id = Label(text=str(employee[0]), color=(
                0, 0, 0, 1), size_hint=(None, 1), width=100)
            f_name = Label(text=employee[1], color=(0, 0, 0, 1))
            l_name = Label(text=employee[2], color=(0, 0, 0, 1))
            location = Label(text=employee[3], color=(0, 0, 0, 1))
            clocked_in = Label(text=employee[7], color=(0, 0, 0, 1))
            timestamp = Label(text=employee[8], color=(0, 0, 0, 1))

            label_list.append(
                [emp_id, f_name, l_name, location, clocked_in, timestamp])

        for row in label_list:
            employee_layout = BoxLayout(orientation="horizontal", spacing=0)
            employee_layout.size_hint = (1, None)
            employee_layout.height = 80
            for label in row:
                employee_layout.add_widget(label)
            container.add_widget(employee_layout)

        self.table.add_widget(container)

        return self.table

    def update_table(self, filter=None):
        self.second_layout.remove_widget(self.table)
        self.second_layout.add_widget(self.create_table_container(filter))

    def square_background(self, layout, colour):
        # using the provided layout
        with layout.canvas.before:
            # set colour and create rectangle
            Color(*colour)
            layout.bg = Rectangle(size=layout.size, pos=layout.pos)

    def layout_bg(self, instance, value):
        instance.bg.size = instance.size
        instance.bg.pos = instance.pos


# EmployeeListWindow().run()
