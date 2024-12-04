from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.graphics import Rectangle, Color
from classes.database import Database


class EmployeeListWindow(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Set database object
        self.database = Database()

        # Create main layout and add background colour
        self.main_layout = BoxLayout(orientation="vertical", spacing=0, padding=0)
        self.square_background(self.main_layout, (1, 1, 1, 1))
        self.main_layout.bind(size=self.layout_bg, pos=self.layout_bg)

        # Create second layout for widgets
        self.second_layout = BoxLayout(orientation="vertical", padding=0, spacing=0)

        # Add widgets to layouts
        self.second_layout.add_widget(self.create_button_container())
        self.second_layout.add_widget(self.create_table_container("all"))
        self.main_layout.add_widget(self.create_nav())
        self.main_layout.add_widget(self.second_layout)

        # bind functions to button clicks
        # using lamdba function to be able to pass args into bound functions
        self.all_button.bind(on_press=lambda instance: self.update_table("all"))
        self.clocked_in_button.bind(on_press=lambda instance: self.update_table("clocked in"))
        self.clocked_out_button.bind(on_press=lambda instance: self.update_table("clocked out"))

        # bind function to on enter event to populate table when screen is entered
        self.bind(on_enter=lambda instance: self.update_table("all"))

        # add widget to layout
        self.add_widget(self.main_layout)

    def reset_nav(self, instance, text):
        """ Resets the nav text to default value """
        self.nav_spinner.text = "Menu"

    def switch_screen(self, instance, text):
        """ Switches the app screen based on text passed in """
        # Spinner text passed into function
        original_text = text

        # Checks if passkey is correct and switches screen if so
        def pass_key_response(passkey):
            if passkey == "1234":
                self.manager.current = 'add_employees'
            else:
                self.pop_up_message("Incorrect pass key entered.")

        # Switch screen based on text value
        if original_text == "Add Employee":
            # Opens popup and returns passkey to pass_key_response function
            self.pass_key_popup(pass_key_response)
        elif original_text == "Clock-in/out":
            self.manager.current = "main_window"

        # Reset the nav bar text
        self.reset_nav(instance, text)

    def pass_key_popup(self, callback):

        def on_submit(instance):
            callback(self.pass_key_input.text)
            self.popup_pass_key.dismiss()

        popup_layout = BoxLayout(orientation="vertical", padding=5, spacing=10)

        label = Label(text="Enter pass key")
        self.pass_key_input = TextInput(multiline=False, halign="center")
        button = Button(text="Submit")
        button.bind(on_press=on_submit)

        popup_layout.add_widget(label)
        popup_layout.add_widget(self.pass_key_input)
        popup_layout.add_widget(button)

        self.popup_pass_key = Popup(content=popup_layout, title="Pass Key Check", size_hint=(None,None))
        self.popup_pass_key.size = (500, 400)


        self.popup_pass_key.open()

    def pop_up_message(self, message, time=None):
        """ Create a pop up box with meassage & timestamp if required """
        # Create the layout
        popup_layout = BoxLayout(orientation="vertical")

        # Alter message if timestamp has been passed into the function
        if time:
            message = f"{message} at {time}"
        else:
            message = message

        # Create lable with message text
        message_label = Label(text=message)
        # Create button to close popup
        close_button = Button(text="Close")
        # Add widgets to layout
        popup_layout.add_widget(message_label)
        popup_layout.add_widget(close_button)

        # Create popup object
        popup = Popup(
            title="Message",
            content=popup_layout,
            size_hint=(None, None),
            size=(720, 300),
        )
        # open the popup object
        popup.open()
        # close the popup on close button press
        close_button.bind(on_press=popup.dismiss)

    def create_nav(self):
        """ Create navigation layout and add dropdown widget for selection """
        # Create layout and add background colour
        container = BoxLayout(orientation="vertical")
        self.square_background(container, (0.129, 0.129, 0.129, 1))
        container.bind(size=self.layout_bg, pos=self.layout_bg)
        # Set the size of the layout
        container.size_hint = (1, None)
        container.height = 100

        # Create the dropdown
        self.nav_spinner = Spinner(text="Menu", values=["Clock-in/out", "Add Employee"])
        # Bind switch screen function to dropdown selection
        self.nav_spinner.bind(text=self.switch_screen)
        # Add widget to layout
        container.add_widget(self.nav_spinner)

        return container

    def create_button_container(self):
        """ Create button layout and add buttons to re-query table data """
        # Create the layout and set the background colour
        container = BoxLayout(orientation="horizontal", padding=10)
        self.square_background(container, (0.129, 0.129, 0.129, 1))
        container.bind(size=self.layout_bg, pos=self.layout_bg)
        # Set layout size
        container.size_hint = (1, None)
        container.height = 100
        # Create buttons
        self.all_button = Button(text="All")
        self.clocked_in_button = Button(text="Clocked-in")
        self.clocked_out_button = Button(text="Clocked-out")
        # Add widgets to layout
        container.add_widget(self.all_button)
        container.add_widget(self.clocked_in_button)
        container.add_widget(self.clocked_out_button)

        return container

    def create_table_container(self, filter=None):
        """ Creates layout and widgets for table """

        # Create scrollable layout
        self.table = ScrollView(size_hint=(1, 1))
        # Create layout for headers a data
        container = BoxLayout(orientation="vertical", size_hint_y=None, spacing=10, padding=10)
        container.bind(minimum_height=container.setter("height"))

        # Create header layout and background colour
        header_layout = BoxLayout(orientation="horizontal")
        self.square_background(header_layout, (0.7, 0.7, 0.7, 0.7))
        header_layout.bind(size=self.layout_bg, pos=self.layout_bg)
        # Set header lauyout size
        header_layout.size_hint = (1, None)
        header_layout.height = 60
        container.add_widget(header_layout)

        # Set table headers
        headers = ["First Name", "Last Name", "Location", "Clocked-in", "Timestamp",]

        # Create the id label with fixed width
        id_label = Label(text='ID', size_hint=(None, 1), width=100)
        id_label.color = (0, 0, 0, 1)
        header_layout.add_widget(id_label)

        # loop through headers and reate a label for each
        for header in headers:
            label = Label(text=header)
            label.color = (0, 0, 0, 1)
            header_layout.add_widget(label)

        # Get the employee data from database
        employees = self.database.get_all_records(filter)
        # Create empty list for rows of data
        label_list = []

        # Loop though all rows of data in employees and create labels for spesific data
        for employee in employees:
            emp_id = Label(text=str(employee[0]), color=(
                0, 0, 0, 1), size_hint=(None, 1), width=100)
            f_name = Label(text=employee[1], color=(0, 0, 0, 1))
            l_name = Label(text=employee[2], color=(0, 0, 0, 1))
            location = Label(text=employee[3], color=(0, 0, 0, 1))
            clocked_in = Label(text=employee[7], color=(0, 0, 0, 1))
            timestamp = Label(text=employee[8], color=(0, 0, 0, 1))

            # Append a list for each row of data needed for table
            label_list.append([emp_id, f_name, l_name, location, clocked_in, timestamp])

        # Loop though each row in label list create a layout and set the side
        for row in label_list:
            employee_layout = BoxLayout(orientation="horizontal", spacing=0)
            employee_layout.size_hint = (1, None)
            employee_layout.height = 60
            # Loop through each label in the row and add the label to layout
            for label in row:
                employee_layout.add_widget(label)

            # add employee layout to the container layout
            container.add_widget(employee_layout)

        # add contaienr layout the table layout
        self.table.add_widget(container)

        return self.table

    def update_table(self, filter=None):
        """ Remove the table widget and then re-adds it with updated data """
        self.second_layout.remove_widget(self.table)
        self.second_layout.add_widget(self.create_table_container(filter))

    def square_background(self, layout, colour):
        # using the provided layout
        with layout.canvas.before:
            # set colour and create rectangle
            Color(*colour)
            layout.bg = Rectangle(size=layout.size, pos=layout.pos)

    def layout_bg(self, instance, value):
        # using the provided layout set the instance size to the current size
        instance.bg.size = instance.size
        instance.bg.pos = instance.pos
