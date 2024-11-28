from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.graphics import Rectangle, Color
from database import Database


class EmployeeListWindow(App):
    def build(self):

        self.database = Database()

        self.main_layout = BoxLayout(orientation="vertical", spacing=0, padding=0)
        self.main_background(self.main_layout, (1, 1, 1, 1))

        self.second_layout = BoxLayout(orientation="vertical", padding=0, spacing=0)

        self.second_layout.add_widget(self.create_button_container())
        self.second_layout.add_widget(self.create_table_container("all"))
        self.main_layout.add_widget(self.create_nav())
        self.main_layout.add_widget(self.second_layout)

        self.all_button.bind(on_press=lambda instance: self.update_table("all"))
        self.clocked_in_button.bind(
            on_press=lambda instance: self.update_table("clocked in")
        )
        self.clocked_out_button.bind(
            on_press=lambda instance: self.update_table("clocked out")
        )

        return self.main_layout

    def create_nav(self):
        container = BoxLayout(orientation="vertical")
        self.square_background(container, (0.129, 0.129, 0.129, 1))
        container.bind(size=self.layout_bg, pos=self.layout_bg)
        container.size_hint = (1, None)
        container.height = 100

        nav_button = Spinner(text="Nav", values=["Clock-in/out", "Add Employee"])
        container.add_widget(nav_button)

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
            "ID",
            "First Name",
            "Last Name",
            "Location",
            "Clocked-in",
            "Timestamp",
        ]

        for header in headers:
            label = Label(text=header, size_hint=(1, None))
            label.color = (0, 0, 0, 1)
            header_layout.add_widget(label)

        employees = self.database.get_all_records(filter)

        label_list = []

        for employee in employees:
            emp_id = Label(text=str(employee[0]), color=(0, 0, 0, 1))
            f_name = Label(text=employee[1], color=(0, 0, 0, 1))
            l_name = Label(text=employee[2], color=(0, 0, 0, 1))
            location = Label(text=employee[3], color=(0, 0, 0, 1))
            clocked_in = Label(text=employee[4], color=(0, 0, 0, 1))
            timestamp = Label(text="time stamp", color=(0, 0, 0, 1))

            label_list.append([emp_id, f_name, l_name, location, clocked_in, timestamp])

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

    def main_background(self, layout, colour):
        # using the provided layout
        with layout.canvas.before:
            # set colour and create rectangle
            Color(*colour)
            self.main_layout_bg = Rectangle(size=layout.size, pos=layout.pos)
        # set size and position of main background to layout size / pos
        layout.bind(size=self.update_main_layout_bg, pos=self.update_main_layout_bg)

    def update_main_layout_bg(self, instance, value):
        self.main_layout_bg.size = instance.size
        self.main_layout_bg.pos = instance.pos


EmployeeListWindow().run()
