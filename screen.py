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
from kivymd.uix.menu import MDDropdownMenu


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
        :param instance: Determine where the click happen on the (MDFloatingActionButtonSpeedDial)
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
        :return: None
        """
        automate = Automate(filename)
        self.workbook_data = automate.get_workbook_data()
        self.screen_transition_editor()
        self.manager.render_wb_data(render_data=self.workbook_data)

    def screen_transition_editor(self):
        """
        Defining the screen transition towards the editor screen
        :return: None
        """
        self.manager.transition.direction = "left"
        self.manager.current = "editor_screen"

    def toolbar_menu_sheets(self):
        """
        Defining the menu bar for the MDDropDownItem/sheets ->
        (Which give the information about the sheets).
        :return: None
        """
        sheets = self.workbook_data["sheets"]
        drop_down_menu = MDDropdownMenu(
            caller=self.ids.drop_item_sheets,
            items=[{"text": str(sheets[i]), "font_name": "assets/font/Heebo-Regular/ttf"}
                    for i in range(len(sheets))
                   ],
            width_mult=4
        )
        drop_down_menu.bind(on_release=self.drop_down_menu_callback)
        drop_down_menu.open()

    def toolbar_menu_tools(self):
        """
        Defining the menu bar for the MDDropDownItem/tools ->
        (Which give the information about the tools).
        :return: None
        """
        automation_tool = ["Apply formulas", "Sort", "Reverse", "Delete", "Merge sheet"]
        drop_down_menu = MDDropdownMenu(
            caller=self.ids.drop_item_tools,
            items=[{"text": str(automation_tool[i]), "font_name": "assets/font/Heebo-Regular/ttf"}
                   for i in range(len(automation_tool))
                   ],
            width_mult=4
        )
        drop_down_menu.bind(on_release=self.drop_down_menu_callback)
        drop_down_menu.open()

    def drop_down_menu_callback(self, instance_menu, instance_menu_item):
        """
        Receive the input from the mentioned drop_down_menu
        :param instance_menu: Instance of the menu on which users click.
        :param instance_menu_item: Instance of the menu_item on which users click.
        :return: None
        """
        pass


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
        :return: 
        """
        self.manager.transition.direction = "right"
        self.manager.current = "home_screen"
