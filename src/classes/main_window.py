from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.graphics import Rectangle, Color, RoundedRectangle
from kivy.core.window import Window
from kivy.uix.popup import Popup
from classes.database import Database
import datetime


class MainWindow(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Set title and database object
        self.title = "Pendle Doors Clock-in System"
        self.database = Database()
        self.padding_value = Window.width * 0.02

        # Set main layout of window
        main_layout = BoxLayout(orientation="vertical", spacing=self.padding_value)
        # Set background colour of window
        self.square_background(main_layout, (1, 1, 1, 1))
        main_layout.bind(size=self.update_container_bg, pos=self.update_container_bg)

        second_layout = BoxLayout(orientation="vertical", padding=self.padding_value, spacing=self.padding_value)

        # Add containers to main layout
        main_layout.add_widget(self.create_nav())
        main_layout.add_widget(second_layout)
        second_layout.add_widget(self.create_details_container())
        self.employees_on_site()
        second_layout.add_widget(self.create_location_container())
        second_layout.add_widget(BoxLayout(size_hint=(1, None), height=50))
        second_layout.add_widget(self.create_button_container())
        second_layout.add_widget(self.create_message_container())

        self.add_widget(main_layout)

    def create_nav(self):
        """ Creates a layout for the navigation bar and adds dropdown widget """
        # Create the layout & set the background colour
        container = BoxLayout(orientation="vertical")
        self.square_background(container, (0.129, 0.129, 0.129, 1))
        container.bind(size=self.update_container_bg, pos=self.update_container_bg)
        # Set layout height
        container.size_hint = (1, None)
        container.height = 80

        # Create nav dropdown
        self.nav_spinner = Spinner(text="Menu", values=["Add Employee", "Employee List"])
        # bind scqitch screen func to dropdown selection
        self.nav_spinner.bind(text=self.switch_screen)
        # Add widget to layout
        container.add_widget(self.nav_spinner)

        return container

    def create_details_container(self):
        """ Creates a layout and adds widgets for the details section """
        # Create layout & add background colour
        container = BoxLayout(orientation="vertical", padding=self.padding_value)
        container.size_hint = (1, None)
        container.height = 250
        self.rounded_background(container, (0.7, 0.7, 0.7, 0.7))
        container.bind(size=self.update_container_bg, pos=self.update_container_bg)
        # Set details label text and create label
        details_text = "Company: Pendle Doors"
        self.details_label = Label(text=details_text, color=(0, 0, 0, 1))
        # add label to widget
        container.add_widget(self.details_label)

        return container

    def create_location_container(self):
        """ Creates a layout & adds widgets for the location selection """
        # create layout
        container = BoxLayout(orientation="vertical", padding=(50, 20, 50, 20))
        # set fixed height
        container.size_hint = (1, None)
        container.height = 150
        # create rectanle for background colour
        self.rounded_background(container, (0.7, 0.7, 0.7, 0.7))
        # set rectangle size and postition to window size / pos
        container.bind(size=self.update_container_bg, pos=self.update_container_bg)
        # Create spinner (combobox) set values and default value
        self.location_spinner = Spinner(values=["Mill Bank", "Moss Fold"])
        self.location_spinner.size_hint = (1, None)
        self.location_spinner.height = 60
        self.location_spinner.text = "Select a location"
        # add spinnder to layout
        container.add_widget(self.location_spinner)

        return container

    def create_button_container(self):
        """ Creates a layout and adds widgets for the clock-in/put buttons """
        # set container layout
        container = BoxLayout(orientation="vertical", padding=(50, 20, 50, 20), spacing=20)
        container.size_hint = (1, None)
        container.height = 350
        # add rectangle for background colour
        self.rounded_background(container, (0.7, 0.7, 0.7, 0.7))
        # set rectangle size and position to window size / pos
        container.bind(size=self.update_container_bg, pos=self.update_container_bg)

        # create employee id label & input
        id_input_label = Label(text="Enter employee ID to clock in.")
        id_input_label.color = (0, 0, 0, 1)
        self.id_input = TextInput()
        self.id_input.size_hint = (1, None)
        self.id_input.height = 60
        self.id_input.multiline = False
        self.id_input.halign = "center"
        self.id_input.padding = 17.5
        self.id_input.font_size = 25
        # Create clock in button
        clock_in_button = Button(text="Clock-in", size_hint=(1, None))
        clock_in_button.height = 60
        clock_in_button.background_normal = ""
        clock_in_button.background_color = (56 / 255, 161 / 255, 24 / 255)
        clock_in_button.on_press = self.clock_in
        # Create clock out button
        clock_out_button = Button(text="Clock-out", size_hint=(1, None))
        clock_out_button.height = 60
        clock_out_button.background_normal = ""
        clock_out_button.background_color = (158 / 255, 28 / 255, 25 / 255)
        clock_out_button.on_press = self.clock_out
        # add widgets to layout
        container.add_widget(id_input_label)
        container.add_widget(self.id_input)
        container.add_widget(clock_in_button)
        container.add_widget(clock_out_button)

        return container

    def create_message_container(self):
        # set container layout
        container = BoxLayout(orientation="vertical")
        # add rectangle for background colour
        self.rounded_background(container, (0.7, 0.7, 0.7, 0.7))
        container.bind(size=self.update_container_bg, pos=self.update_container_bg)

        # create message lable
        self.message_label = Label(color=(0, 0, 0, 1))
        current_date = str(datetime.datetime.now().strftime("%d/%m/%Y"))
        self.message_label.text = f"Today's date: {current_date}"
        # add label to widget
        container.add_widget(self.message_label)

        return container

    def reset_nav(self, instance, text):
        """ Resets the navigation text for after selection """
        instance.text = "Menu"

    def switch_screen(self, instance, text):
        """ Switches the screen based on instance text """
        # get the text from the spinner
        original_text = text

        # Checks if passkey is correct and switches screen if so
        def pass_key_response(passkey):
            if passkey == "1234":
                self.manager.current = 'add_employees'
            else:
                self.pop_up_message("Incorrect pass key entered.")

        # switches the screen based on the text
        if original_text == "Employee List":
            self.manager.current = "employee_list_window"

        elif original_text == "Add Employee":
            # Opens popup and returns passkey to pass_key_response function
            self.pass_key_popup(pass_key_response)

        # resets the nav text back to Menu
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

        self.popup_pass_key = Popup(content=popup_layout, title=self.title, size_hint=(None,None))
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

    def pop_up_user_check(self, name, direction, callback):
        """ creates a popup to check if you are about to clock in/out the intended person """

        # Nested functions to set callback to True or False depending on the button press
        def on_yes(instance):
            callback(True)
            popup.dismiss()

        def on_no(instance):
            callback(False)
            popup.dismiss()
        
        # Create popup layouts
        popup_layout = BoxLayout(orientation="vertical")
        button_layout = BoxLayout(orientation="horizontal")

        # Check direction passed into fucntion and set message accordingly
        if direction == "in":
            message_text = f"You are about to clock in {name}, is this correct?"
        else:
            message_text = f"You are about to clock out {name}, is this correct?"
        
        # Create message label
        message_label = Label(text=message_text)

        # Create buttons
        button_yes = Button(text="Yes")
        button_no = Button(text="No")

        # Add widgest to layout
        button_layout.add_widget(button_yes)
        button_layout.add_widget(button_no)
        popup_layout.add_widget(message_label)
        popup_layout.add_widget(button_layout)

        # Create popup object
        popup = Popup(title="Message", content=popup_layout)
        popup.size_hint = (None, None)
        popup.size = (720, 300)

        # bind the nested functions the the buttons
        button_yes.bind(on_press=on_yes)
        button_no.bind(on_press=on_no)

        # Open the popup
        popup.open()

    def employees_on_site(self):
        """ Get the number of employees for each site and update the details label """
        # Run count function for number of employees at sites
        employees_onsite = self.database.count_employess_on_site()

        # Get values of employees at each site
        self.mill_bank_on_site = employees_onsite["Mill Bank"]
        self.moss_fold_on_site = employees_onsite["Moss Fold"]

        # Set the details text inclduding clocked in employee count
        details_text = f"""Company: Pendle Doors\n\nMill Bank employees on site: {
            self.mill_bank_on_site}\nMoss Fold employees on site: {self.moss_fold_on_site}"""

        # Apply detail text to label
        self.details_label.text = details_text

    def clock_in(self):

        def user_check_response(response):
            """Handles response to pop up yes or no button selection"""
            if response:  # if response is true
                # Clock in user
                self.database.clock_in(self.location_spinner.text, employee["ID"])
                # Set clock in message
                message = f"{employee['Name']} has just clocked in at {self.location_spinner.text}"
                self.id_input.text = ""  # Clear id input
                self.pop_up_message(message)  # execute popup with message
                self.employees_on_site()  # re-count employees on sites for details container
                self.location_spinner.text = ("Select a location")  # reset the spinner text
            else:
                self.pop_up_message("Clock-in canceled by user.")
                self.location_spinner.text = ("Select a location")  # reset the spinner text

        # if a location has been selected
        if self.id_input.text != "":
            if self.location_spinner.text != "Select a location":
                # Get employee details
                employee = self.database.employee_details(self.id_input.text)
                # if employee is found
                if employee is not None:
                    # and if they are not already clocked in
                    if not self.database.check_clocked_in(employee["ID"]):
                        # Pop up for confirmation of user clock in
                        self.pop_up_user_check(employee["Name"], "in", user_check_response)
                    else:
                        # if user already clocked in set message
                        message = f"{employee['Name']} is already clocked in at {
                            self.location_spinner.text}."
                        self.id_input.text = ""  # clear id input
                        # execute popup with message
                        self.pop_up_message(message)

                    self.employees_on_site()  # re-count employees on sites
                else:
                    self.pop_up_message("No user with ID input.")
            else:
                # display popup message if no location is selected
                self.pop_up_message("Please select a location to clock in.")
        else:
            self.pop_up_message("No ID input.")

    def clock_out(self):

        def user_check_response(response):
            """Handles response to pop up yes or no button selection"""
            if response:  # if response is true
                # Clock out user
                self.database.clock_out(employee["ID"])
                # Set clock out message
                message = f"{employee['Name']} has just clocked out."
                self.id_input.text = ""  # Clear id input
                self.pop_up_message(message)  # execute popup with message
                self.employees_on_site()  # re-count employees on sites for details container
                self.location_spinner.text = (
                    "Select a location"  # reset the spinner text
                )
            else:
                self.pop_up_message("Clock-out canceled by user.")
                self.location_spinner.text = (
                    "Select a location"  # reset the spinner text
                )

        if self.id_input.text != "":
            # Get employee details
            employee = self.database.employee_details(self.id_input.text)
            # if employee is found
            if employee is not None:
                # and if they are clocked in
                if self.database.check_clocked_in(employee["ID"]):
                    # Pop up for confirmation of user clock in
                    self.pop_up_user_check(employee["Name"], "in", user_check_response)
                else:
                    # if user already clocked in set message
                    message = f"{employee['Name']} is already clocked out."
                    self.id_input.text = ""  # clear id input
                    self.pop_up_message(message)  # execute popup with message

                self.employees_on_site()  # re-count employees on sites
            else:
                self.pop_up_message("No user with ID input.")
        else:
            self.pop_up_message("No ID input.")

    def rounded_background(self, layout, colour):
        # using layout passed into function set colour and create rounded rectangle
        with layout.canvas.before:
            Color(*colour)
            layout.bg = RoundedRectangle(size=layout.size, pos=layout.pos, radius=[20])

    def square_background(self, layout, colour):
        # using the provided layout
        with layout.canvas.before:
            # set colour and create rectangle
            Color(*colour)
            layout.bg = Rectangle(size=layout.size, pos=layout.pos)

    def update_container_bg(self, instance, value):
        # using the layout passed into function, set layout size to current instance size
        instance.bg.size = instance.size
        instance.bg.pos = instance.pos

    def current_time(self):
        time_str = str(datetime.datetime.now().strftime("%X"))
        return time_str
