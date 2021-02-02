"""
--------------------------------------------------------->
Copyrights (c) to UR's tech.ltd. All rights reserved
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
        if self.ids.rail.rail_state == "open":
            self.ids.rail.rail_state = "close"
        else:
            self.ids.rail.rail_state = "open"

    def open_file_manager(self, instance):
        if instance.icon == "assets/images/add.png":
            tk_root = Tk()
            tk_root.eval(f"tk::PlaceWindow {tk_root.winfo_toplevel()} center")
            tk_root.withdraw()
            file_manager = filedialog.askopenfile(title="Open workbook", filetypes=((".xlsx", "*.xlsx"),))
            if file_manager is not None:
                filename = file_manager.name
                self.open_workbook(filename)

    @staticmethod
    def open_workbook(filename):
        automate = Automate(filename)
        workbook_data = automate.get_workbook_data()
        print(workbook_data)


class HomeScreen(Base):
    pass


class SettingScreen(Base):
    pass


class TutorialScreen(Base):
    pass


class EditorScreen(Screen):
    pass
