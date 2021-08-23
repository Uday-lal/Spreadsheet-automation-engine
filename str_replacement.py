"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Perform inspection of string in the merged data
"""
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRectangleFlatButton
from kivy.utils import get_color_from_hex


class StrReplacement:
    def __init__(self, wb_data, str_index_data, equal_to_index):
        self.wb_data = wb_data
        self.str_index_data = str_index_data
        self.equal_to_index = equal_to_index
        self.is_overwrite = False
        self.raised_merge_conflict = False
        self.operation_registry = {}

    def perform_replacement(self):
        """
        Replace strings with its empty string
        or its original value
        :return: list
        """
        for index in self.str_index_data:
            ri, ci, cell_value = index[0]
            self.wb_data[ri - 1][ci][0] = cell_value
            self.wb_data[ri - 1][self.equal_to_index][0] = ""
        return self.wb_data

    def perform_equal_to_replacement(self, column_actual_values, total, editor_screen):
        """
        Replace strings with its empty string
        or its original value at where we have
        a existing column
        :param editor_screen:
        :param column_actual_values: Column index contain string value and its index
        in equal to column
        :param total: The total coming from the execution
        :return: list
        """
        self.operation_registry["column_index"] = column_actual_values
        self.operation_registry["total"] = total
        self.editor_screen = editor_screen
        self.operation_registry["editor_screen"] = self.editor_screen
        for index in self.str_index_data:
            ci, ri, cell_value = index[0]
            self.wb_data[ci - 1][ri][0] = cell_value

        if column_actual_values:
            for index in column_actual_values:
                i1, i2, cell_value = index
                corresponding_total_value_index = self.index_parser(index_pair=(i1, i2))
                if corresponding_total_value_index is None:
                    if not self.raised_merge_conflict:
                        self.raise_merge_conflict()
                        break
                if self.is_overwrite:
                    self.wb_data[i1][i2][0] = total[i1 - 1]
                else:
                    self.wb_data[i1][i2][0] = cell_value

        return self.wb_data

    def raise_merge_conflict(self):
        self.dialog = MDDialog(
            text="Merge conflict raised during while processing current instructions. Do you want to",
            buttons=[
                MDRectangleFlatButton(
                    text="Overwrite",
                    theme_text_color="Custom",
                    text_color=get_color_from_hex("#9962d1"),
                    line_color=get_color_from_hex("#702ab8")
                ),
                MDRectangleFlatButton(
                    text="Don't overwrite",
                    theme_text_color="Custom",
                    text_color=get_color_from_hex("#9962d1"),
                    line_color=get_color_from_hex("#702ab8")
                ),
            ]
        )
        self.dialog.buttons[0].bind(on_release=lambda instance: self.dialog_callback(instance=instance))
        self.dialog.buttons[1].bind(on_release=lambda instance: self.dialog_callback(instance=instance))
        self.dialog.open()

    def dialog_callback(self, instance):
        self.dialog.dismiss()
        self.raised_merge_conflict = True
        if instance.text == "Overwrite":
            self.is_overwrite = True
        else:
            self.is_overwrite = False
        self.wb_data = self.perform_equal_to_replacement(
            column_actual_values=self.operation_registry["column_index"],
            total=self.operation_registry["total"],
            editor_screen=self.operation_registry["editor_screen"]
        )
        self.editor_screen.manager.reload_dashboard(data=self.wb_data)

    def index_parser(self, index_pair):
        """
        Parse the closest index from the str_index_data
        :param index_pair: Pair of parsing index
        :return: tuple
        """
        ip1, ip2 = index_pair
        for index in self.str_index_data:
            ci, ri, cell_value = index[0]
            ci -= 1
            if ip1 == ci:
                return ci, ri
