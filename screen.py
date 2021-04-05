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
from kivy.core.window import Window
from Automate.coc_engine.executor import Executor
from components import MsgSnackBar, Item, CancelButton
from kivymd.uix.bottomsheet import MDGridBottomSheet
from kivy.utils import get_color_from_hex
from kivymd.uix.dialog import MDDialog
from selection_mode import SelectionMode


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
    selection_mode = BooleanProperty(False)
    operation_type = StringProperty()

    def __init__(self, **kwargs):
        super(EditorScreen, self).__init__(**kwargs)
        self.cancel_button = CancelButton()

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
        automation_tool = [  # Defining tool and icon respectively (tool, icon)
            ("Apply formulas", "math-integral-box"),
            ("Sort", "sort"),
            ("Reverse", "sort-reverse-variant"),
            ("Delete", "delete")
        ]
        self.bottom_sheet = MDGridBottomSheet()
        for tool in automation_tool:
            self.bottom_sheet.add_item(
                text=tool[0],
                callback=lambda tool=tool[0]: self.bottom_sheet_callback(instance=tool),
                icon_src=tool[1]
            )
        self.bottom_sheet.radius = 30
        self.bottom_sheet.icon_size = "35sp"
        self.bottom_sheet.radius_from = "top"
        self.bottom_sheet.open()

    def bottom_sheet_callback(self, instance):
        """
        Callback to the toolbar_menu_tools ↑
        :param instance: The instance of button which is clicked
        :return: None
        """
        self.selection_mode = True
        self.ids.rail.md_bg_color = get_color_from_hex("#702ab8")
        self.ids.tool_bar.title = f"Selected {instance.caption}"
        snack_bar = MsgSnackBar(
            text=f"Select at least two column the apply {instance.caption} operation",
            snackbar_x="10dp",
            snackbar_y="10dp"
        )
        if instance.caption == "Apply formulas":
            apply_formula_operation = ["Addition", "Subtraction", "Multiplication", "Division"]
            self.dialog = MDDialog(
                title="Select mathematical operation",
                type="simple",
                items=[
                    Item(text=operation)
                    for operation in apply_formula_operation
                ]
            )
            self.dialog.open()
        elif instance.caption == "Sort":
            self.operation_type = "Sort"
            snack_bar.open()
        elif instance.caption == "Reverse":
            self.operation_type = "Reverse"
            snack_bar.open()
        elif instance.caption == "Delete":
            self.operation_type = "Delete"
            snack_bar.open()

    def list_item_callback(self, selected_math_operation):
        """
        Defining the callback to the
        dialog item object
        :param selected_math_operation: Text of list item
        :return: None
        """
        self.dialog.dismiss()
        snack_bar = MsgSnackBar(
            text=f"Select at least two column the apply {selected_math_operation} operation",
            snackbar_x="10dp",
            snackbar_y="10dp"
        )
        self.ids.command_palette.text = "new"
        self.ids.tool_bar.title = f"Apply formulas/{selected_math_operation}"
        self.ids.main_tool_bar.add_widget(self.cancel_button)
        snack_bar.open()
        if selected_math_operation == "Addition":
            self.operation_type = "Apply formulas/add"
        elif selected_math_operation == "Multiplication":
            self.operation_type = "Apply formulas/multiply"
        elif selected_math_operation == "Division":
            self.operation_type = "Apply formulas/divide"
        elif selected_math_operation == "Subtraction":
            self.operation_type = "Apply formulas/sub"

    def drop_down_menu_callback(self, instance_menu, instance_menu_item):
        """
        Receive the input from the mentioned drop_down_menu
        :param instance_menu: Instance of the menu on which users click.
        :param instance_menu_item: Instance of the menu_item on which users click.
        :return: str
        """
        dropdown_menu = instance_menu.caller
        selected_item = instance_menu_item.text
        dropdown_menu.set_item(f"Sheets/{selected_item}")
        self.manager.update_dashboard(selected_sheet=selected_item)
        self.drop_down_menu_sheets.dismiss()

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
        if not self.selection_mode:
            data = self.manager.render_data
            apply_selection = ApplySelection(data=data[self.manager.current_sheet]["rows"])
            self.master_selected_data = apply_selection.master_selection(cell=cell)
            self.manager.reload_dashboard(data=data[self.manager.current_sheet]["rows"])
        else:
            master_cell = cell
            if "Apply formulas" not in self.operation_type and not master_cell.text.isdigit():
                data = self.manager.render_data
                apply_selection = ApplySelection(data=data[self.manager.current_sheet]["rows"])
                self.master_selected_data = apply_selection.master_selection(cell=cell)
                self.ids.command_palette.text = master_cell.text
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
        if not self.selection_mode:
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
            if not self.selection_mode:
                if self.validate_commands:
                    headers = self.manager.render_data[self.manager.current_sheet]["rows"][0]
                    self.data_for_execution = CoordinateOperationController(
                        headers=headers,
                        commands=command
                    ).provide_data_for_execution()
                    self.executor()
                else:
                    snack_bar = MsgSnackBar(
                        text="Invalid command! System refuse to accept this command",
                        snackbar_x="10dp",
                        snackbar_y="10dp"
                    )
                    snack_bar.size_hint_x = (Window.width - (snack_bar.snackbar_x * 2)) / Window.width
                    snack_bar.open()
            else:
                selection_mode = SelectionMode(
                    wb_data=self.manager.render_data[self.manager.current_sheet]["rows"],
                    selected_data=self.master_selected_data,
                    equal_to=command,
                    operation_type=self.operation_type,
                    max_rc=(
                        self.manager.render_data[self.manager.current_sheet]["max_row"],
                        self.manager.render_data[self.manager.current_sheet]["max_cols"]
                    )
                )
                selection_mode.execute()
                updated_data = selection_mode.marge()
                self.remove_selection_mode()
                self.manager.reload_dashboard(data=updated_data)

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
        executor.execute()
        updated_data = executor.marge()
        self.manager.reload_dashboard(data=updated_data)

    def remove_selection_mode(self):
        """
        Reset everything thing after
        selection mode
        :return: None
        """
        self.selection_mode = False
        self.ids.tool_bar.title = "Edit workbook"
        self.ids.main_tool_bar.remove_widget(self.cancel_button)
        self.ids.rail.md_bg_color = get_color_from_hex("#9962d1")
        self.unselect_master_selections()
