from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Rectangle, Color, RoundedRectangle
from kivy.uix.spinner import Spinner
from kivy.uix.gridlayout import GridLayout


class AddEmployees(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.title = "Add Employees"

        main_layout = BoxLayout(orientation="vertical", spacing=0, padding=0)
        self.square_background(main_layout, (1, 1, 1, 1))
        main_layout.bind(size=self.update_container_bg,
                         pos=self.update_container_bg)

        second_layout = BoxLayout(
            orientation="vertical", spacing=20, padding=20)

        second_layout.add_widget(self.create_input_container())
        second_layout.add_widget(self.create_button_container())
        second_layout.add_widget(BoxLayout())

        main_layout.add_widget(self.create_nav())
        main_layout.add_widget(second_layout)

        self.add_widget(main_layout)

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
        container.height = 100

        nav_spinner = Spinner(text="Menu", values=[
                              "Clock-in/out", "Employee List"])
        nav_spinner.bind(text=self.switch_screen)
        container.add_widget(nav_spinner)

        return container

    def create_button_container(self):
        container = BoxLayout(orientation="vertical", spacing=20, padding=20)
        self.rounded_background(container, (0.7, 0.7, 0.7, 0.7))
        container.bind(size=self.update_container_bg,
                       pos=self.update_container_bg)
        container.size_hint = (1, None)
        container.height = 200

        create_button = Button(text="Create")
        clear_button = Button(text="Clear")
        container.add_widget(create_button)
        container.add_widget(clear_button)

        return container

    def create_input_container(self):
        main_c_layout = BoxLayout(orientation='vertical')
        self.rounded_background(main_c_layout, (0.7, 0.7, 0.7, 0.7))
        main_c_layout.bind(size=self.update_container_bg,
                           pos=self.update_container_bg)

        container = BoxLayout(orientation="horizontal",
                              spacing=20, padding=(100, 0, 100, 100))

        title_label = Label(text="Fill out the below to add a new employee",
                            size_hint=(1, None), height=80, color=(0, 0, 0, 1))

        label_container = GridLayout(cols=1, spacing=20, padding=20)
        label_container.size_hint = (None, 1)
        label_container.width = 300
        input_container = GridLayout(cols=1, spacing=20, padding=20)
        input_container2 = GridLayout(cols=1, spacing=20, padding=20)

        labels = ["First name", "Last name",
                  "Department", "Shift start", "Shift end"]

        for label in labels:
            new_label = Label(text=label)
            new_label.color = (0, 0, 0, 1)
            new_label.size_hint = (None, None)
            new_label.height = 80
            new_label.width = 300

            label_container.add_widget(new_label)

        f_name_input = TextInput(
            size_hint=(1, None), height=80, padding=(10, 10, 10, 10)
        )
        f_name_input.multiline = False
        f_name_input.font_size = 40
        l_name_input = TextInput(size_hint=(1, None), height=80)
        l_name_input.multiline = False
        l_name_input.font_size = 40

        departments = [
            "Sales",
            "Veneer Line",
            "CNC",
            "Rework",
            "Bespoke",
            "Paint",
            "Technical",
            "Directors",
            "Logistics",
        ]
        departments.sort()
        dept_input = Spinner(values=departments,
                             size_hint=(1, None), height=80)

        am = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09"]
        hours = am + [str(n) for n in range(10, 25)]
        minutes = am + [str(n) for n in range(10, 61)]

        s_start_hour = Spinner(text="08:00", values=hours,
                               size_hint=(1, None), height=80)
        s_end_hour = Spinner(text="17:00", values=hours,
                             size_hint=(1, None), height=80)
        s_start_mins = Spinner(text="00:00", values=minutes,
                               size_hint=(1, None), height=80)
        s_end_mins = Spinner(text="00:00", values=minutes,
                             size_hint=(1, None), height=80)

        input_container.add_widget(f_name_input)
        input_container.add_widget(l_name_input)
        input_container.add_widget(dept_input)
        input_container.add_widget(s_start_hour)
        input_container.add_widget(s_end_hour)
        input_container2.add_widget(Label(size_hint=(1, None), height=80))
        input_container2.add_widget(Label(size_hint=(1, None), height=80))
        input_container2.add_widget(Label(size_hint=(1, None), height=80))
        input_container2.add_widget(s_start_mins)
        input_container2.add_widget(s_end_mins)

        container.add_widget(label_container)
        container.add_widget(input_container)
        container.add_widget(input_container2)

        main_c_layout.add_widget(title_label)
        main_c_layout.add_widget(container)

        return main_c_layout

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