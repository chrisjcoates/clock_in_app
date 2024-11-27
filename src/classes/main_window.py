from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.graphics import Rectangle, Color, RoundedRectangle
from kivy.uix.popup import Popup
from classes.database import Database
import datetime


class MainWindow(App):
    def build(self):

        self.title = "Pendle Doors Clock-in System"

        # Set main layout of window
        main_layout = BoxLayout(orientation="vertical", padding=25, spacing=20)
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

    def pop_up_message(self, message, time=None):

        popup_layout = BoxLayout(orientation="vertical")

        if time:
            message = f"{message} at {time}"
        else:
            message = message

        message_label = Label(text=message)
        close_button = Button(text="Close")

        popup_layout.add_widget(message_label)
        popup_layout.add_widget(close_button)

        popup = Popup(
            title="Message",
            content=popup_layout,
            size_hint=(None, None),
            size=(900, 300),
        )

        popup.open()

        close_button.bind(on_press=popup.dismiss)

    def pop_up_user_check(self, name, direction, callback):

        result = {"Value": None}

        def on_yes(instance):
            callback(True)
            popup.dismiss()

        popup_layout = BoxLayout(orientation="vertical")
        button_layout = BoxLayout(orientation="horizontal")

        if direction == "in":
            message_text = f"You are about to clock in {name}, is this correct?"
        else:
            message_text = f"You are about to clock out {name}, is this correct?"

        message_label = Label(text=message_text)

        button_yes = Button(text="Yes")
        button_no = Button(text="No")

        button_layout.add_widget(button_yes)
        button_layout.add_widget(button_no)

        popup_layout.add_widget(message_label)
        popup_layout.add_widget(button_layout)

        popup = Popup(title="Message", content=popup_layout)
        popup.size_hint = (None, None)
        popup.size = (900, 300)

        button_yes.bind(on_press=on_yes)

        button_no.bind(on_press=popup.dismiss)

        popup.open()

        return result

    def employees_on_site(self):

        # Open database
        database = Database()
        # Run count function for number of employees at sites
        employees_onsite = database.count_employess_on_site()

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
                database.clock_in(self.location_spinner.text, employee["ID"])
                # Set clock in message
                message = f"{employee['Name']} has just clocked in at {self.location_spinner.text}"
                self.id_input.text = ""  # Clear id input
                self.pop_up_message(message)  # execute popup with message
                self.employees_on_site()  # re-count employees on sites for details container
                self.location_spinner.text = (
                    "select a location"  # reset the spinner text
                )
            else:
                self.pop_up_message("Clock-in canceled by user.")

        # if a location has been selected
        if self.location_spinner.text != "Select a location":
            # Open database
            database = Database()
            # Get employee details
            employee = database.employee_details(self.id_input.text)
            # if employee is found
            if employee is not None:
                # and if they are not already clocked in
                if not database.check_clocked_in(employee["ID"]):
                    # Pop up for confirmation of user clock in
                    self.pop_up_user_check(employee["Name"], "in", user_check_response)
                else:
                    # if user already clocked in set message
                    message = f"{employee['Name']} is already clocked in at {self.location_spinner.text}."
                    self.id_input.text = ""  # clear id input
                    self.pop_up_message(message)  # execute popup with message

                self.employees_on_site()  # re-count employees on sites
        else:
            # display popup message if no location is selected
            self.pop_up_message("Please select a location to clock in.")

    def clock_out(self):
        # Open database
        database = Database()
        # get employee details
        employee = database.employee_details(self.id_input.text)

        # if employee is found
        if employee != None:
            # and employee is clocked in
            if database.check_clocked_in(employee["ID"]):

                # Prompt to confirm here

                database.clock_out(employee["ID"])  # clock out employee
                # set message for clock out
                message = f"{employee['Name']} has just clocked out"
                self.id_input.text = ""  # reset id input text

                # set the current time and execute popup with message
                current_time = self.current_time()
                self.pop_up_message(message, current_time)

            else:
                # of employee is already clocked out
                # Set message
                message = f"{employee['Name']} is already clocked out"
                self.id_input.text = ""  # reset id input text
                # execute popup meassge
                self.pop_up_message(message)
            # reset the location input text
            self.location_spinner.text = "Select a location"

            self.employees_on_site()  # re-count employees on site

    def create_details_container(self):
        # set container layout
        container = BoxLayout(orientation="vertical")
        # create rectangle for background colour
        self.rounded_background(container, (0.7, 0.7, 0.7, 0.7))
        # set rectangle size and position to window size / pos
        container.bind(size=self.update_details_bg, pos=self.update_details_bg)
        # Set details label text and create label
        details_text = "Company: Pendle Doors"
        self.details_label = Label(text=details_text, color=(0, 0, 0, 1))
        # add label to widget
        container.add_widget(self.details_label)

        return container

    def create_location_container(self):
        # create layout
        container = BoxLayout(orientation="vertical", padding=50)
        # set fixed height
        container.size_hint = (1, None)
        container.height = 200
        # create rectanle for background colour
        self.rounded_background(container, (0.7, 0.7, 0.7, 0.7))
        # set rectangle size and postition to window size / pos
        container.bind(size=self.update_location_bg, pos=self.update_location_bg)
        # Create spinner (combobox) set values and defsutl value
        self.location_spinner = Spinner(values=["Mill Bank", "Moss Fold"])
        self.location_spinner.text = "Select a location"
        # add spinnder to layout
        container.add_widget(self.location_spinner)

        return container

    def create_button_container(self):
        # set container layout
        container = BoxLayout(orientation="vertical", padding=50, spacing=20)
        # add rectangle for background colour
        self.rounded_background(container, (0.7, 0.7, 0.7, 0.7))
        # set rectangle size and position to window size / pos
        container.bind(size=self.update_button_bg, pos=self.update_button_bg)

        # crete employee id input
        id_input_label = Label(text="Enter employee ID to clock in.")
        id_input_label.color = (0, 0, 0, 1)
        self.id_input = TextInput()
        # Create clock in / out buttons
        clock_in_button = Button(text="Clock-in")
        clock_in_button.background_normal = ""
        clock_in_button.background_color = (56 / 255, 161 / 255, 24 / 255)
        clock_in_button.on_press = self.clock_in
        clock_out_button = Button(text="Clock-out")
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
        container.bind(size=self.update_message_bg, pos=self.update_message_bg)

        # create message lable
        self.message_label = Label(color=(0, 0, 0, 1))
        current_date = str(datetime.datetime.now().strftime("%d/%m/%Y"))
        self.message_label.text = f"Today's date: {current_date}"
        # add label to widget
        container.add_widget(self.message_label)

        return container

    def main_background(self, layout, colour):
        # using the provided layout
        with layout.canvas.before:
            # set colour and create rectangle
            Color(*colour)
            self.main_layout_bg = Rectangle(size=layout.size, pos=layout.pos)
        # set size and position of main background to layout size / pos
        layout.bind(size=self.update_main_layout_bg, pos=self.update_main_layout_bg)

    def rounded_background(self, layout, colour):
        # using layot provided set colour and create rounded rectangle
        with layout.canvas.before:
            Color(*colour)
            layout.bg = RoundedRectangle(size=layout.size, pos=layout.pos, radius=[20])

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

    def current_time(self):
        time_str = str(datetime.datetime.now().strftime("%X"))
        return time_str
