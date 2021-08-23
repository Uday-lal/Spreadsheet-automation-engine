"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Defining the editor screen
"""


import os
from . import Base

from kivy.properties import (
    NumericProperty,
    BooleanProperty,
    StringProperty,
    ListProperty
)

from kivy.utils import get_color_from_hex

from Automate.coc_engine import CoordinateOperationController
from Automate.coc_engine.executor import Executor
from Automate.coc_engine.validate import Validator
from components import Item, CancelButton
from components import NotOverwriteDialogContent
from errors import *
from kivymd.uix.bottomsheet import MDGridBottomSheet
from kivymd.uix.button import MDRectangleFlatButton, MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu
from mof_library.apply_selection_mof import ApplySelection
from selection_mode import SelectionMode
from selection_mode_validation import SelectionModeValidation


class EditorScreen(Base):
    drop_down_tool_bar_height = NumericProperty()
    validate_commands = BooleanProperty()  # Commands inserted in the command palette
    selection_mode = BooleanProperty(False)
    operation_type = StringProperty()
    master_selected_data = ListProperty()

    def __init__(self, **kwargs):
        super(EditorScreen, self).__init__(**kwargs)
        self.cancel_button = CancelButton()
        self.str_index_data = None

    def back_to_home(self):
        """
        Define back to home screen functionality
        :return: None
        """
        self.manager.transition.direction = "right"
        self.manager.current = "home_screen"
        self.ids.drop_item_sheets.text = "Sheets"
        self.manager.clear_dashboard()

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
                    "font_name": "assets/fonts/Heebo-Regular.ttf",
                    "viewclass": "OneLineListItem",
                    "on_release": lambda sheet=sheets[i]: self.drop_down_menu_callback(
                        instance_menu=self.ids.drop_item_sheets,
                        selected_menu_item=sheet
                    )
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

        try:
            self.ids.main_tool_bar.add_widget(self.cancel_button)
        except Exception:
            self.ids.main_tool_bar.remove_widget(self.cancel_button)
            self.ids.main_tool_bar.add_widget(self.cancel_button)

        self.cancel_button.bind(on_release=lambda instance: self.remove_selection_mode())
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
        snack_bar.size_hint_x = (Window.width - (snack_bar.snackbar_x * 2)) / Window.width
        snack_bar.open()
        if selected_math_operation == "Addition":
            self.operation_type = "Apply formulas/add"
        elif selected_math_operation == "Multiplication":
            self.operation_type = "Apply formulas/multiply"
        elif selected_math_operation == "Division":
            self.operation_type = "Apply formulas/divide"
        elif selected_math_operation == "Subtraction":
            self.operation_type = "Apply formulas/sub"

    def drop_down_menu_callback(self, instance_menu, selected_menu_item):
        """
        Receive the input from the mentioned drop_down_menu
        :param instance_menu: Instance of the menu on which users click.
        :param selected_menu_item: Selected menu item on which users click.
        :return: str
        """
        dropdown_menu = instance_menu
        selected_item = selected_menu_item
        dropdown_menu.text = f"Sheets/{selected_item}"
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
            try:
                _text_field_data = int(text_field_data)
            except ValueError:
                _text_field_data = text_field_data
            data = self.manager.render_data
            current_sheet = self.manager.current_sheet
            data[current_sheet]["rows"][cell.row_index][cell.column_index][0] = _text_field_data
            self.manager.reload_dashboard(data=data[current_sheet]["rows"])

    def master_selection(self, cell):
        """
        Making master selection and change the dashboard
        accordingly
        :param cell: Cell object
        :return: None
        """
        is_row_merging = True if cell.text.isdigit() else False
        self.master_cell = cell
        if not self.master_cell.text.isdigit():
            if not self.selection_mode or "Apply formulas" in self.operation_type:
                data = self.manager.render_data
                apply_selection = ApplySelection(data=data[self.manager.current_sheet]["rows"]) if not \
                    self.selection_mode else \
                    ApplySelection(data=data[self.manager.current_sheet]["rows"], is_perform_inspection=True)
                try:
                    is_data_merged = True
                    try:
                        apply_selection.implement_mof(cell=self.master_cell)
                    except Exception as e:
                        if str(e) == "We can't perform arithmetic on strings or words":
                            is_data_merged = False
                            snack_bar = MsgSnackBar(
                                text=str(e),
                                snackbar_x="10dp",
                                snackbar_y="10dp"
                            )
                            snack_bar.size_hint_x = (Window.width - (snack_bar.snackbar_x * 2)) / Window.width
                            snack_bar.open()
                            self.remove_selection_mode()

                    selected_wb_data = apply_selection.merge(is_row_merging=is_row_merging)
                    self.manager.master_selected_data.append(apply_selection.get_merged_data())
                    if type(selected_wb_data) is not tuple:
                        data[self.manager.current_sheet]["rows"] = selected_wb_data
                    else:
                        data[self.manager.current_sheet]["rows"], self.str_index_data = selected_wb_data
                        self.manager.str_index_data.append(self.str_index_data)
                        if not is_data_merged:
                            for str_index_data in self.str_index_data:
                                if str_index_data == "Exception":
                                    break
                                ci, ri, cell_value = str_index_data
                                data[self.manager.current_sheet]["rows"][ci - 1][ri][0] = cell_value
                except ValueError:
                    pass
                self.manager.reload_dashboard(data=data[self.manager.current_sheet]["rows"])
            else:
                if "Apply formulas" not in self.operation_type:
                    if not self.master_cell.text.isdigit():
                        data = self.manager.render_data
                        apply_selection = ApplySelection(data=data[self.manager.current_sheet]["rows"])
                        apply_selection.implement_mof(cell=self.master_cell)
                        selected_wb_data = apply_selection.merge(is_row_merging=is_row_merging)
                        self.manager.master_selected_data.append(apply_selection.get_merged_data())
                        self.master_selected_data = self.manager.master_selected_data
                        data[self.manager.current_sheet]["rows"] = selected_wb_data
                        self.ids.command_palette.text = self.master_cell.text
                        self.manager.reload_dashboard(data=data[self.manager.current_sheet]["rows"])
                    else:
                        rows_selection_error()
        else:
            rows_selection_error()

    def unselect_master_selections(self):
        """
        Unselecting the selected all the cell
        if users click to other self or navigate
        to a other screen
        :return: None
        """
        data = self.manager.render_data
        apply_selection = ApplySelection(data=data[self.manager.current_sheet]["rows"])
        apply_selection.implement_mof_for_unselect()
        data[self.manager.current_sheet]["rows"] = apply_selection.merge(is_row_merging=False)
        self.manager.reload_dashboard(data=data[self.manager.current_sheet]["rows"])

    def validate(self, command):
        """
        Validate the insert command
        :param command: Inserted command
        :return: None
        """
        headers = self.manager.render_data[self.manager.current_sheet]["rows"][0]
        if not self.selection_mode:
            self.validate_commands = Validator(
                headers=headers,
                max_rows=self.manager.render_data[self.manager.current_sheet]["max_row"],
                command=command
            ).validate()
        else:
            self.validate_commands = SelectionModeValidation(command=command, headers=headers).validate()
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
                self.master_selected_data = self.manager.master_selected_data
                if self.master_selected_data:
                    try:
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
                        updated_data = selection_mode.marge(editor_screen=self) if self.str_index_data == [] else \
                            selection_mode.marge(editor_screen=self, str_index_data=self.manager.str_index_data)
                        self.remove_selection_mode()
                        self.manager.reload_dashboard(data=updated_data)
                        self.manager.master_selected_data.clear()
                        self.manager.str_index_data.clear()
                    except Exception:
                        something_went_wrong()
                else:
                    snack_bar = MsgSnackBar(
                        text="Please select some column",
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
        try:
            executor = Executor(
                sheet_data=self.manager.render_data[self.manager.current_sheet]["rows"],
                data_for_execution=self.data_for_execution
            )
            executor.execute()
            updated_data = executor.marge(editor_screen=self)
            self.manager.reload_dashboard(data=updated_data)
        except Exception as e:
            if str(e) == "We can't perform arithmetic on strings or words" \
                    or str(e) == "System dose not accept this input":
                snack_bar = MsgSnackBar(
                    text=str(e),
                    snackbar_x="10dp",
                    snackbar_y="10dp"
                )
                snack_bar.size_hint_x = (Window.width - (snack_bar.snackbar_x * 2)) / Window.width
                snack_bar.open()
            else:
                something_went_wrong()

    def remove_selection_mode(self):
        """
        Reset everything thing after
        selection mode
        :return: None
        """
        self.selection_mode = False
        self.manager.master_selected_data.clear()
        self.ids.tool_bar.title = "Edit workbook"
        self.ids.command_palette.text = ""
        self.ids.main_tool_bar.remove_widget(self.cancel_button)
        self.ids.rail.md_bg_color = get_color_from_hex("#9962d1")
        self.unselect_master_selections()

    def save_dialog(self):
        dialog_button_option = ["Overwrite", "Don't overwrite", "Cancel"]
        self._save_dialog = MDDialog(
            text="Do you want to overwrite this workbook?",
            buttons=[
                MDRectangleFlatButton(
                    text=button_option,
                    theme_text_color="Custom",
                    text_color=get_color_from_hex("#9962d1"),
                    line_color=get_color_from_hex("#702ab8")
                )
                for button_option in dialog_button_option
            ]
        )
        self._save_dialog.buttons[0].bind(
            on_release=lambda instance: self.save_dialog_callback(button_instance=instance))
        self._save_dialog.buttons[1].bind(
            on_release=lambda instance: self.save_dialog_callback(button_instance=instance))
        self._save_dialog.buttons[2].bind(
            on_release=lambda instance: self.save_dialog_callback(button_instance=instance))
        self._save_dialog.open()

    def save_dialog_callback(self, button_instance):
        """
        Defining the callback of save dialog
        :param button_instance: Dialog button instance
        :return: None
        """
        if button_instance.text == "Overwrite":
            self.manager.save()
            self.manager.transition.direction = "right"
            self.manager.current = "home_screen"
            self.manager.clear_home_screen()
            self.manager.render_home_screen_content()
        elif button_instance.text == "Don't overwrite":
            self._save_dialog.dismiss()
            self.not_overwrite_dialog = MDDialog(
                title="Enter workbook name",
                type="custom",
                content_cls=NotOverwriteDialogContent(),
                buttons=[
                    MDFlatButton(
                        text="CANCEL", text_color=get_color_from_hex("#525252")
                    ),
                    MDFlatButton(
                        text="Save", text_color=get_color_from_hex("#525252")
                    ),
                ],
            )
            self.not_overwrite_dialog.buttons[0].bind(
                on_release=lambda instance: self.not_overwrite_dialog_callback(
                    instance=instance,
                    content_cls_instance=self.not_overwrite_dialog.content_cls
                )
            )
            self.not_overwrite_dialog.buttons[1].bind(
                on_release=lambda instance: self.not_overwrite_dialog_callback(
                    instance=instance,
                    content_cls_instance=self.not_overwrite_dialog.content_cls
                )
            )
            self.not_overwrite_dialog.open()
        self._save_dialog.dismiss()

    def not_overwrite_dialog_callback(self, instance, content_cls_instance):
        """
        Defining the callback of not_overwrite_dialog
        :param instance: Not overwrite dialog instance
        :param content_cls_instance: Content class instance of not overwrite dialog
        :return: None
        """
        if instance.text == "Save":
            new_filename = str(content_cls_instance.ids.filename_field.text) + ".xlsx"
            content_cls_instance.ids.filename_field.text = ""
            file_path = self.manager.render_data["file_path"]
            path, filename = os.path.split(file_path)
            updated_path = str(path) + "/" + new_filename
            self.manager.save(updated_path=updated_path)
            self.manager.transition.direction = "right"
            self.manager.current = "home_screen"
            self.manager.clear_home_screen()
            self.manager.render_home_screen_content()
        self.not_overwrite_dialog.dismiss()
