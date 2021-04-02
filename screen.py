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
from kivy.properties import (
    NumericProperty,
    BooleanProperty,
    StringProperty
)
from apply_selection import ApplySelection
from Automate.coc_engine import CoordinateOperationController
from Automate.coc_engine.validate import Validator
from kivymd.uix.snackbar import BaseSnackbar
from kivy.core.window import Window
from Automate.coc_engine.executor import Executor


class ErrorSnackBar(BaseSnackbar):
    """Shows the command on the screen"""
    text = StringProperty(None)
    icon = StringProperty(None)
    font_size = NumericProperty("15sp")


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
    validate_commands = BooleanProperty()  # Commands inserted in the command palette

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
            items=[
                {
                    "text": str(sheets[i]),
                    "font_name": "assets/fonts/Heebo-Regular.ttf"
                }
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
            items=[
                {
                    "text": str(automation_tool[i]),
                    "font_name": "assets/fonts/Heebo-Regular.ttf"
                }
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
            print(processing_data)
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

    def update_cell(self, text_field_data, cell):
        """
        Take the text field data on the
        popup and apply some logic on it
        :param text_field_data: text field data coming from MDTextField
        :param cell: Cell object which is clicked
        :return: None
        """
        if text_field_data != "":
            data = self.manager.render_data
            current_sheet = self.manager.current_sheet
            data[current_sheet]["rows"][cell.row_index][cell.column_index][0] = text_field_data
            self.manager.reload_dashboard(data=data[current_sheet]["rows"])

    def master_selection(self, cell):
        """
        Making master selection and change the dashboard
        accordingly
        :param cell: Cell object
        :return: None
        """
        data = self.manager.render_data
        apply_selection = ApplySelection(data=data[self.manager.current_sheet]["rows"])
        apply_selection.master_selection(cell=cell)
        self.manager.reload_dashboard(data=data[self.manager.current_sheet]["rows"])

    def unselect_master_selections(self):
        """
        Unselecting the selected all the cell
        if users click to other self or navigate
        to a other screen
        :return: None
        """
        data = self.manager.render_data
        apply_selection = ApplySelection(data=data[self.manager.current_sheet]["rows"])
        apply_selection.unselect()
        self.manager.reload_dashboard(data=data[self.manager.current_sheet]["rows"])

    def validate(self, command):
        """
        Validate the insert command
        :param command: Inserted command
        :return: None
        """
        headers = self.manager.render_data[self.manager.current_sheet]["rows"][0]
        self.validate_commands = Validator(
            headers=headers,
            max_rows=self.manager.render_data[self.manager.current_sheet]["max_row"],
            command=command
        ).validate()
        if self.validate_commands:
            self.ids.command_palette._primary_color = (0, 1, 0, 1)
        else:
            self.ids.command_palette._primary_color = (1, 0, 0, 1)

    def execute_command(self, command):
        """
        Given the validated command to
        the coc engine
        :param command: Command for execution
        :return: None
        """
        if command != "":
            if self.validate_commands:
                headers = self.manager.render_data[self.manager.current_sheet]["rows"][0]
                self.data_for_execution = CoordinateOperationController(
                    headers=headers,
                    commands=command
                ).provide_data_for_execution()
                print(self.data_for_execution)
                self.executor()
            else:
                snack_bar = ErrorSnackBar(
                    text="Invalid command! System refuse to accept this command",
                    icon="alert",
                    snackbar_x="10dp",
                    snackbar_y="10dp"
                )
                snack_bar.size_hint_x = (Window.width - (snack_bar.snackbar_x * 2)) / Window.width
                snack_bar.open()

    def executor(self):
        """
        Execute the ins instructions coming from
        coc engine
        :return: None
        """
        executor = Executor(
            sheet_data=self.manager.render_data[self.manager.current_sheet]["rows"],
            data_for_execution=self.data_for_execution
        )
