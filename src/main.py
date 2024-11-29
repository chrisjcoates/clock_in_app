from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, NoTransition
from classes.main_window import MainWindow
from classes.employee_list import EmployeeListWindow
from classes.add_employees import AddEmployees


class ClockingApp(App):
    def build(self):

        self.title = "Clocking-in/out System"

        screen_mananger = ScreenManager()
        screen_mananger.transition = NoTransition()

        screen_mananger.add_widget(MainWindow(name="main_window"))
        screen_mananger.add_widget(
            EmployeeListWindow(name="employee_list_window"))
        screen_mananger.add_widget(AddEmployees(name="add_employees"))

        screen_mananger.current = "main_window"

        return screen_mananger


if __name__ == "__main__":
    window = ClockingApp()
    window.run()


# todos

# Create add employee window
