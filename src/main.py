from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, NoTransition
from classes.main_window import MainWindow
from classes.employee_list_window import EmployeeListWindow


class ScreenSwitcherApp(App):
    def build(self):

        sm = ScreenManager()
        sm.transition = NoTransition()

        sm.add_widget(MainWindow(name="main_window"))
        sm.add_widget(EmployeeListWindow(name="employee_list_window"))

        sm.current = "main_window"

        return sm


if __name__ == "__main__":
    window = ScreenSwitcherApp()
    window.run()


# todos

# Create add employee window
