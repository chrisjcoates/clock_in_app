from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivy.core.window import Window
from classes.main_window import MainWindow
from classes.employee_list import EmployeeListWindow
from classes.add_employees import AddEmployees


class ClockingApp(App):
    def build(self):
        # Set the window size
        Window.size = (800, Window.height)
        # set the window title
        self.title = "Clocking-in/out System"

        # Create a screen manager
        screen_mananger = ScreenManager()
        # Remove transition from screen manager for instant screen switching
        screen_mananger.transition = NoTransition()

        # Add screen objects to the screen manager
        screen_mananger.add_widget(MainWindow(name="main_window"))
        screen_mananger.add_widget(EmployeeListWindow(name="employee_list_window"))
        screen_mananger.add_widget(AddEmployees(name="add_employees"))

        # set the current screen for when application opens
        screen_mananger.current = "main_window"

        return screen_mananger


if __name__ == "__main__":
    window = ClockingApp()
    window.run()


# todos
