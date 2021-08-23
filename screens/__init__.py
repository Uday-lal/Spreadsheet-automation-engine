"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Defining all the screen used in this app
"""


from kivy.uix.screenmanager import Screen
from tkinter import filedialog
from Automate import Automate
from tkinter import *


class Base(Screen):
    def rail_open(self):
        """
        Control the state of the MDNavigationRail
        :return: None
        """
        if self.ids.rail.rail_state == "open":
            self.ids.rail.rail_state = "close"
        else:
            self.ids.rail.rail_state = "open"

    def open_file_manager(self):
        """
        Open the file manager
        :return: None
        """
        tk_root = Tk()
        tk_root.eval(f"tk::PlaceWindow {tk_root.winfo_toplevel()} center")
        tk_root.withdraw()
        file_manager = filedialog.askopenfile(title="Open workbook", filetypes=((".xlsx", "*.xlsx"),))
        if file_manager is not None:
            self.filename = file_manager.name
            self.open_workbook()

    def get_wb_data(self):
        """
        Get the data from the selected workbook.
        :return: dict
        """
        automation = Automate(filename=self.filename)
        return automation.get_workbook_data()

    def open_workbook(self):
        """
        Get data from the workbook
        :return: None
        """
        self.manager.render_wb_data(render_data=self.get_wb_data())
        self.screen_transition_editor()

    def screen_transition_editor(self):
        """
        Defining the screen transition towards the editor screen
        :return: None
        """
        self.manager.transition.direction = "left"
        self.manager.current = "editor_screen"
