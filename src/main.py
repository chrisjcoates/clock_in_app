from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, NoTransition
from classes.main_window import MainWindow
from classes.employee_list import EmployeeListWindow
from classes.add_employees import AddEmployees


class ClockingApp(App):
    def build(self):

        self.title = "Clocking-in/out System"

        sm = ScreenManager()
        sm.transition = NoTransition()

        sm.add_widget(MainWindow(name="main_window"))
        sm.add_widget(EmployeeListWindow(name="employee_list_window"))
        sm.add_widget(AddEmployees(name="add_employees"))

        sm.current = "main_window"

        return sm


if __name__ == "__main__":
    window = ClockingApp()
    window.run()


# todos

# Create add employee window
