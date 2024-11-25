from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.graphics import Rectangle, Color, RoundedRectangle
from classes.database import Database


class MainWindow(App):
    def build(self):

        self.title = "Pendle Doors Clock-in System"

        # Set main layout of window
        main_layout = BoxLayout(orientation='vertical',
                                padding=25, spacing=20)
        # Set background colour of window
        self.main_background(main_layout, (1, 1, 1, 1))

        # Add containers to main layout
        main_layout.add_widget(self.create_details_container())
        self.employees_on_site()
        main_layout.add_widget(self.create_location_container())
        main_layout.add_widget(BoxLayout(size_hint=(1, None), height=150))
        main_layout.add_widget(self.create_button_container())
        main_layout.add_widget(self.create_message_container())

        return main_layout

    def employees_on_site(self):

        database = Database()
        employees_onsite = database.count_employess_on_site()

        self.mill_bank_on_site = employees_onsite['Mill Bank']
        self.moss_fold_on_site = employees_onsite['Moss Fold']

        details_text = f"""Company: Pendle Doors\n\nMill Bank employees on site: {
            self.mill_bank_on_site}\nMoss Fold employees on site: {self.moss_fold_on_site}"""

        self.details_label.text = details_text

    def clock_in(self):

        if self.location_spinner.text != 'Select a location':
            database = Database()

            employee = database.employee_details(self.id_input.text)

            if employee != None:

                if not database.check_clocked_in(employee['ID']):
                    database.clock_in(
                        self.location_spinner.text, employee['ID'])

                    message = f"{employee['Name']} has just clocked in"

                    self.message_label.text = message

                    Clock.schedule_once(self.clear_message, 7)
                else:
                    message = f"{employee['Name']} is already Clocked in."

                    self.message_label.text = message

                    Clock.schedule_once(self.clear_message, 7)

                self.location_spinner.text = 'Select a location'

                self.employees_on_site()
        else:
            self.message_label.text = 'Please select a location to clock in.'

            Clock.schedule_once(self.clear_message, 7)

    def clock_out(self):
        database = Database()

        employee = database.employee_details(self.id_input.text)

        if employee != None:

            if database.check_clocked_in(employee['ID']):
                database.clock_out(employee['ID'])

                message = f"{employee['Name']} has just clocked out"

                self.message_label.text = message

                Clock.schedule_once(self.clear_message, 7)
            else:
                message = f"{employee['Name']} is already clocked out"

                self.message_label.text = message

                Clock.schedule_once(self.clear_message, 7)

            self.location_spinner.text = 'Select a location'

            self.employees_on_site()

    def create_details_container(self):
        container = BoxLayout(orientation='vertical')
        self.rounded_background(container, (0.7, 0.7, 0.7, 0.7))
        container.bind(size=self.update_details_bg, pos=self.update_details_bg)

        details_text = 'Company: Pendle Doors'

        self.details_label = Label(text=details_text, color=(0, 0, 0, 1))
        container.add_widget(self.details_label)

        return container

    def create_location_container(self):
        container = BoxLayout(orientation='vertical', padding=50)
        container.size_hint = (1, None)
        container.height = 200
        self.rounded_background(container, (0.7, 0.7, 0.7, 0.7))
        container.bind(size=self.update_location_bg,
                       pos=self.update_location_bg)

        self.location_spinner = Spinner(values=['Mill Bank', 'Moss Fold'])
        self.location_spinner.text = 'Select a location'
        container.add_widget(self.location_spinner)

        return container

    def create_button_container(self):
        container = BoxLayout(orientation='vertical', padding=50, spacing=20)
        self.rounded_background(container, (0.7, 0.7, 0.7, 0.7))
        container.bind(size=self.update_button_bg, pos=self.update_button_bg)

        id_input_label = Label(text='Enter id to clock in.')
        id_input_label.color = (0, 0, 0, 1)
        self.id_input = TextInput()

        clock_in_button = Button(text='Clock-in')
        clock_in_button.background_normal = ''
        clock_in_button.background_color = (56/255, 161/255, 24/255)
        clock_in_button.on_press = self.clock_in
        clock_out_button = Button(text='Clock-out')
        clock_out_button.background_normal = ''
        clock_out_button.background_color = (158/255, 28/255, 25/255)
        clock_out_button.on_press = self.clock_out

        container.add_widget(id_input_label)
        container.add_widget(self.id_input)
        container.add_widget(clock_in_button)
        container.add_widget(clock_out_button)

        return container

    def create_message_container(self):
        container = BoxLayout(orientation='vertical')
        self.rounded_background(container, (0.7, 0.7, 0.7, 0.7))
        container.bind(size=self.update_message_bg, pos=self.update_message_bg)

        self.message_label = Label(
            text='Enter employee ID to clock in or out.', color=(0, 0, 0, 1))
        container.add_widget(self.message_label)

        return container

    def main_background(self, layout, colour):
        with layout.canvas.before:
            Color(*colour)
            self.main_layout_bg = Rectangle(size=layout.size, pos=layout.pos)
        layout.bind(size=self.update_main_layout_bg,
                    pos=self.update_main_layout_bg)

    def rounded_background(self, layout, colour):
        with layout.canvas.before:
            Color(*colour)
            layout.bg = RoundedRectangle(
                size=layout.size, pos=layout.pos, radius=[20])

    def update_main_layout_bg(self, instance, value):
        self.main_layout_bg.size = instance.size
        self.main_layout_bg.pos = instance.pos

    def update_details_bg(self, instance, value):
        instance.bg.size = instance.size
        instance.bg.pos = instance.pos

    def update_location_bg(self, instance, value):
        instance.bg.size = instance.size
        instance.bg.pos = instance.pos

    def update_button_bg(self, instance, value):
        instance.bg.size = instance.size
        instance.bg.pos = instance.pos

    def update_message_bg(self, instance, value):
        instance.bg.size = instance.size
        instance.bg.pos = instance.pos

    def clear_message(self, dt):
        self.message_label.text = 'Enter employee ID to clock in or out.'
