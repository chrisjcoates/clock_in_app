from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Rectangle, Color, RoundedRectangle


class MainWindow(App):
    def build(self):

        # Set main layout of window
        main_layout = BoxLayout(orientation='vertical',
                                padding=25, spacing=20)
        # Set background colour of window
        self.main_background(main_layout, (1, 1, 1, 1))

        # Add containers to main layout
        main_layout.add_widget(self.create_details_container())
        main_layout.add_widget(self.create_location_container())
        main_layout.add_widget(BoxLayout(size_hint=(1, None), height=150))
        main_layout.add_widget(self.create_button_container())
        main_layout.add_widget(self.create_message_container())

        return main_layout

    def create_details_container(self):
        container = BoxLayout(orientation='vertical')
        self.rounded_background(container, (0.7, 0.7, 0.7, 0.7))
        container.bind(size=self.update_details_bg, pos=self.update_details_bg)

        details_label = Label(text='Company: Pendle Doors', color=(0, 0, 0, 1))
        container.add_widget(details_label)

        return container

    def create_location_container(self):
        container = BoxLayout(orientation='vertical', padding=50)
        container.size_hint = (1, None)
        container.height = 200
        self.rounded_background(container, (0.7, 0.7, 0.7, 0.7))
        container.bind(size=self.update_location_bg,
                       pos=self.update_location_bg)

        location_spinner = Spinner(values=['Mill Bank', 'Moss Fold'])
        location_spinner.text = 'Select a location'
        container.add_widget(location_spinner)

        return container

    def create_button_container(self):
        container = BoxLayout(orientation='vertical', padding=50, spacing=20)
        self.rounded_background(container, (0.7, 0.7, 0.7, 0.7))
        container.bind(size=self.update_button_bg, pos=self.update_button_bg)

        clock_in_button = Button(text='Clock-in')
        clock_in_button.background_normal = ''
        clock_in_button.background_color = (56/255, 161/255, 24/255)
        clock_out_button = Button(text='Clock-out')
        clock_out_button.background_normal = ''
        clock_out_button.background_color = (158/255, 28/255, 25/255)

        container.add_widget(clock_in_button)
        container.add_widget(clock_out_button)

        return container

    def create_message_container(self):
        container = BoxLayout(orientation='vertical')
        self.rounded_background(container, (0.7, 0.7, 0.7, 0.7))
        container.bind(size=self.update_message_bg, pos=self.update_message_bg)

        message_label = Label(text='Idle', color=(0, 0, 0, 1))
        container.add_widget(message_label)

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


window = MainWindow()
window.run()
