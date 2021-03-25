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
from Automate import Automate
from kivymd.uix.menu import MDDropdownMenu
from kivy.properties import NumericProperty


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


class HomeScreen(Base):
    pass


class SettingScreen(Base):
    pass


class TutorialScreen(Base):
    pass


class EditorScreen(Base):
    drop_down_tool_bar_height = NumericProperty()

    def back_to_home(self):
        """
        Define back to home screen functionality
        :return: None
        """
        self.manager.transition.direction = "right"
        self.manager.current = "home_screen"

    def toolbar_menu_sheets(self):
        """
        Defining the menu bar for the MDDropDownItem/sheets ->
        (Which give the information about the sheets).
        :return: None
        """
        sheets = self.manager.sheets
        self.drop_down_menu_sheets = MDDropdownMenu(
            caller=self.ids.drop_item_sheets,
            items=[{"text": str(sheets[i]), "font_name": "assets/fonts/Heebo-Regular.ttf"}
                   for i in range(len(sheets))
                   ],
            width_mult=4
        )
        self.drop_down_menu_sheets.bind(on_release=self.drop_down_menu_callback)
        self.drop_down_menu_sheets.open()

    def toolbar_menu_tools(self):
        """
        Defining the menu bar for the MDDropDownItem/tools ->
        (Which give the information about the tools).
        :return: None
        """
        automation_tool = ["Apply formulas", "Sort", "Reverse", "Delete", "Merge sheet"]
        self.drop_down_menu_tool = MDDropdownMenu(
            caller=self.ids.drop_item_tools,
            items=[{"text": str(automation_tool[i]), "font_name": "assets/fonts/Heebo-Regular.ttf"}
                   for i in range(len(automation_tool))
                   ],
            width_mult=4
        )
        self.drop_down_menu_tool.bind(on_release=self.drop_down_menu_callback)
        self.drop_down_menu_tool.open()

    def toolbar_menu_add_column_row(self):
        pass

    def drop_down_menu_callback(self, instance_menu, instance_menu_item):
        """
        Receive the input from the mentioned drop_down_menu
        :param instance_menu: Instance of the menu on which users click.
        :param instance_menu_item: Instance of the menu_item on which users click.
        :return: str
        """
        dropdown_menu = instance_menu.caller
        selected_item = instance_menu_item.text

        if dropdown_menu.text == "Sheets":
            dropdown_menu.set_item(f"Sheets/{selected_item}")
            self.manager.update_dashboard(selected_sheet=selected_item)
            self.drop_down_menu_sheets.dismiss()
        else:
            dropdown_menu.set_item(f"Tools/{selected_item}")
            processing_data = self.dash_board_connection()
            if selected_item == "Apply formulas":
                pass
            elif selected_item == "Sort":
                pass
            elif selected_item == "Reverse":
                pass
            elif selected_item == "Delete":
                pass
            elif selected_item == "Marge sheet":
                pass
            self.drop_down_menu_tool.dismiss()

    def dash_board_connection(self):
        """
        Make a connection between dashboard and
        automation engine for sharing data
        :return: None
        """
        return self.manager.get_selected_data()

    @staticmethod
    def get_popup_field_data(text_field_data):
        """
        Take the text field data on the
        popup and apply some logic on it
        :param text_field_data: text field data coming from MDTextField
        :return: str
        """
        return text_field_data
