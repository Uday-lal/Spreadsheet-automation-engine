"""
--------------------------------------------------------->
Copyrights (c) to UR's tech.ltd 2021. All rights reserved
Author: Uday lal
company: UR's tech.ltd
--------------------------------------------------------->
"""

from kivy.uix.screenmanager import Screen
from tkinter import *
from tkinter import filedialog
from automate import Automate


class Base(Screen):
    flat_icon_button_data = {
        "assets/images/add.png": "Add workbook"
    }

    def rail_open(self):
        """
        Control the state of the MDNavigationRail
        :return: None
        """
        if self.ids.rail.rail_state == "open":
            self.ids.rail.rail_state = "close"
        else:
            self.ids.rail.rail_state = "open"

    def open_file_manager(self, instance):
        """
        Open the file manager
        :param instance: Determine where the click click on the (MDFloatingActionButtonSpeedDial)
        :return: None
        """
        if instance.icon == "assets/images/add.png":
            tk_root = Tk()
            tk_root.eval(f"tk::PlaceWindow {tk_root.winfo_toplevel()} center")
            tk_root.withdraw()
            file_manager = filedialog.askopenfile(title="Open workbook", filetypes=((".xlsx", "*.xlsx"),))
            if file_manager is not None:
                filename = file_manager.name
                self.open_workbook(filename)

    def open_workbook(self, filename):
        """
        Get data from the workbook
        :param filename: path to the excel file
        :return: dict
        """
        automate = Automate(filename)
        workbook_data = automate.get_workbook_data()
        self.screen_transition_editor()
        self.manager.render_wb_data(render_data=workbook_data)
        return workbook_data

    def screen_transition_editor(self):
        """
        Defining the screen transition towards the editor screen
        :return: None
        """
        self.manager.transition.direction = "left"
        self.manager.current = "editor_screen"


class HomeScreen(Base):
    pass


class SettingScreen(Base):
    pass


class TutorialScreen(Base):
    pass


class EditorScreen(Base):
    def back_to_home(self):
        """
        Define back to home screen functionality
        :return: None
        """
        self.manager.transition.direction = "right"
        self.manager.current = "home_screen"
