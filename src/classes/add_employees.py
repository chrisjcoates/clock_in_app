from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Rectangle, Color, RoundedRectangle
from kivy.uix.spinner import Spinner
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from classes.database import Database


class AddEmployees(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.padding_value = Window.width * 0.02

        self.title = "Add Employees"
        self.database = Database()

        main_layout = BoxLayout(orientation="vertical", spacing=0, padding=0)
        self.square_background(main_layout, (1, 1, 1, 1))
        main_layout.bind(size=self.update_container_bg,
                         pos=self.update_container_bg)

        second_layout = BoxLayout(
            orientation="vertical", spacing=20, padding=20)

        second_layout.add_widget(self.create_input_container())

        main_layout.add_widget(self.create_nav())
        main_layout.add_widget(second_layout)

        self.add_widget(main_layout)

    def create_employee(self, instance):
        f_name = self.f_name_input.text.capitalize()
        l_name = self.l_name_input.text.capitalize()
        dept = self.dept_spinner.text.capitalize()
        s_start = f"{self.s_hours_spinner.text}:{self.s_mins_spinner.text}"
        s_end = f"{self.e_hours_spinner.text}:{self.e_mins_spinner.text}"

        if f_name and l_name and dept:
            if isinstance(f_name, str) and isinstance(l_name, str) and isinstance(dept, str):
                self.database.create_employee(
                    f_name, l_name, dept, s_start, s_end)
                self.clear_employee()
            else:
                print("Employee details include invalid characters.")
        else:
            print('Employee details missing')

    def clear_employee(self, instance=None):
        self.f_name_input.text = ''
        self.l_name_input.text = ''
        self.dept_spinner.text = ''
        self.s_hours_spinner.text = "08"
        self.s_mins_spinner.text = "00"
        self.e_hours_spinner.text = "17"
        self.e_mins_spinner.text = "00"

    def reset_nav(self, instance, text):
        instance.text = "Menu"

    def switch_screen(self, instance, text):

        original_text = text

        if original_text == "Clock-in/out":
            self.manager.current = "main_window"

        elif original_text == "Employee List":
            self.manager.current = 'employee_list_window'

        self.reset_nav(instance, text)

    def create_nav(self):
        container = BoxLayout(orientation="vertical")
        self.square_background(container, (0.129, 0.129, 0.129, 1))
        container.bind(size=self.update_container_bg,
                       pos=self.update_container_bg)
        container.size_hint = (1, None)
        container.height = 80

        nav_spinner = Spinner(text="Menu", values=[
                              "Clock-in/out", "Employee List"])
        nav_spinner.bind(text=self.switch_screen)
        container.add_widget(nav_spinner)

        return container

    def create_input_container(self):

        main_layout = BoxLayout(orientation="vertical",
                                padding=self.padding_value, spacing=20)

        details_layout = GridLayout(
            cols=2, padding=(20, 20, 50, 20), spacing=20)
        self.rounded_background(details_layout, (0.7, 0.7, 0.7, 0.7))
        details_layout.bind(size=self.update_container_bg,
                            pos=self.update_container_bg)

        details_layout.size_hint = (1, None)
        details_layout.height = 250

        shift_layout = GridLayout(
            cols=3, padding=(20, 20, 50, 20), spacing=20)
        shift_layout.size_hint = (1, None)
        shift_layout.height = 200

        self.rounded_background(shift_layout, (0.7, 0.7, 0.7, 0.7))
        shift_layout.bind(size=self.update_container_bg,
                          pos=self.update_container_bg)

        button_layout = BoxLayout(
            orientation="horizontal", padding=(50, 20, 50, 20), spacing=20)
        self.rounded_background(button_layout, (0.7, 0.7, 0.7, 0.7))
        button_layout.bind(size=self.update_container_bg,
                           pos=self.update_container_bg)

        button_layout.size_hint = (1, None)
        button_layout.height = 100

        f_name_label = Label(text="First Name", color=(
            0, 0, 0, 1), size_hint=(1, None), height=60)
        l_name_label = Label(text="Last Name", color=(
            0, 0, 0, 1), size_hint=(1, None), height=60)
        dept_label = Label(text="Department", color=(
            0, 0, 0, 1), size_hint=(1, None), height=60)

        self.f_name_input = TextInput(size_hint=(1, None), height=60)
        self.f_name_input.multiline = False
        self.f_name_input.font_size = 25
        self.l_name_input = TextInput(size_hint=(1, None), height=60)
        self.l_name_input.multiline = False
        self.l_name_input.font_size = 25

        spin_values = ['Bespoke', 'Rework', 'Paint',
                       'Logistics', 'Technical', 'Directors', 'Sales', 'CNC']
        spin_values.sort()
        self.dept_spinner = Spinner(
            text="Select department", values=spin_values, size_hint=(1, None), height=60)

        s_start_label = Label(text="Shift start", color=(0, 0, 0, 1))
        s_end_label = Label(text="Shift end", color=(0, 0, 0, 1))

        nums = ['00', '01', "02", "03", "04", "05", "06", "07", "08", "09"]

        spinner_hours = nums + [str(n) for n in range(10, 24)]
        spinner_mins = nums + [str(n) for n in range(10, 61)]

        self.s_hours_spinner = Spinner(text="08",
                                       values=spinner_hours, size_hint=(1, None), height=60)
        self.s_mins_spinner = Spinner(text="00",
                                      values=spinner_mins, size_hint=(1, None), height=60)

        self.e_hours_spinner = Spinner(text="17",
                                       values=spinner_hours, size_hint=(1, None), height=60)
        self.e_mins_spinner = Spinner(text="00",
                                      values=spinner_mins, size_hint=(1, None), height=60)

        submit_button = Button(text='Submit', size_hint=(1, None), height=60)
        submit_button.bind(on_press=self.create_employee)
        clear_button = Button(text="Clear", size_hint=(1, None), height=60)
        clear_button.bind(on_press=self.clear_employee)

        details_layout.add_widget(f_name_label)
        details_layout.add_widget(self.f_name_input)
        details_layout.add_widget(l_name_label)
        details_layout.add_widget(self.l_name_input)
        details_layout.add_widget(dept_label)
        details_layout.add_widget(self.dept_spinner)

        shift_layout.add_widget(s_start_label)
        shift_layout.add_widget(self.s_hours_spinner)
        shift_layout.add_widget(self.s_mins_spinner)
        shift_layout.add_widget(s_end_label)
        shift_layout.add_widget(self.e_hours_spinner)
        shift_layout.add_widget(self.e_mins_spinner)

        button_layout.add_widget(submit_button)
        button_layout.add_widget(clear_button)

        main_layout.add_widget(details_layout)
        main_layout.add_widget(shift_layout)
        main_layout.add_widget(button_layout)
        main_layout.add_widget(BoxLayout())

        return main_layout

    def rounded_background(self, layout, colour):
        # using layot provided set colour and create rounded rectangle
        with layout.canvas.before:
            Color(*colour)
            layout.bg = RoundedRectangle(
                size=layout.size, pos=layout.pos, radius=[20])

    def square_background(self, layout, colour):
        # using the provided layout
        with layout.canvas.before:
            # set colour and create rectangle
            Color(*colour)
            layout.bg = Rectangle(size=layout.size, pos=layout.pos)

    def update_container_bg(self, instance, value):
        instance.bg.size = instance.size
        instance.bg.pos = instance.pos
