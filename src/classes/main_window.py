from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.graphics import Rectangle, Color, RoundedRectangle


class Main_Window(App):
    def build(self):

        # Set main layout of window
        main_layout = BoxLayout(orientation='vertical')

        # Drawn rectanle to create background colour
        with main_layout.canvas.before:
            Color(50 / 255, 52 / 255, 52 / 255, 1)
            self.main_bg = Rectangle(
                # Set the rectangle size to window size
                size=main_layout.size, pos=main_layout.pos)
        # Bind function to main layout to keep rectangle the same size as window
        main_layout.bind(size=self.update_main_bg, pos=self.update_main_bg)

        return main_layout

    def update_main_bg(self, instance, value):
        # Takes an obect instance and sets the rectangle to the size and postition of the instance
        self.main_bg.size = instance.size
        self.main_bg.pos = instance.pos


window = Main_Window()
window.run()
