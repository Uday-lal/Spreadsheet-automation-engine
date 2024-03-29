"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Validating the users inserted commands
"""
from .clean_command import CleanCommand
import re


class Validator:
    def __init__(self, headers, max_rows, command):
        self.command = CleanCommand(commands=command).shape_input()
        self.headers = headers
        self.max_rows = max_rows
        self.not_excepted_special_char = ["!", "@", "#", "$", "%", "^", "&", "_", "'", "[", "]", "{",
                                          "}", ":", ";", "<", ">", ",", "?", "|", "\\", "\""]
        self.operators = {
            "+": "add",
            "-": "sub",
            "/": "divide",
            "*": "multiply",
            "=": "equal_to"
        }

    def validate(self):
        """
        Validating the user commands
        :return: bool
        """
        count_equal_to_ok = self.count_equal_to()
        coc_order_ok = self.coc_order()
        check_coordinate_ok = self.check_coordinate()
        assign_error_ok = self.assign_error()
        parentheses_validate_ok = self.validate_parentheses()
        if coc_order_ok and count_equal_to_ok and check_coordinate_ok and assign_error_ok and parentheses_validate_ok:
            return True
        else:
            return False

    def count_equal_to(self):
        """
        Counting the equal_to operator
        it should not be more than one
        :return: bool
        """
        equal_to_count = self.count_index(selected_item="=")
        if equal_to_count is None:
            equal_to_count = []
        if len(equal_to_count) == 0:
            return True
        if len(equal_to_count) != 1 or self.command.index("=") != 1:
            return False
        return True

    def coc_order(self):
        """
        Check the command order
        it should be arrange in
        coc pattern
        :return: bool
        """
        for i, command in enumerate(self.command):
            if command == "(" or command == ")":
                return True
            if i == 0 and command in self.operators.keys():
                return False
            if command in self.operators.keys():
                try:
                    next_value = self.command[i + 1]
                    if next_value in self.operators.keys():
                        return False
                except IndexError:
                    pass
            else:
                try:
                    if command in self.not_excepted_special_char:
                        return False
                    next_value = self.command[i + 1]
                    if next_value == ".":
                        return True
                    if next_value not in self.operators.keys():
                        return False
                except IndexError:
                    pass
        return True

    def check_coordinate(self):
        """
        Validate the input coordinate
        :return: bool
        """
        headers = [header[0] for header in self.headers]

        for command in self.command:
            if len(command) == 1:
                if command == "(":
                    return True
                if not command.isdigit():
                    if command not in self.operators.keys():
                        if command not in headers:
                            return False
            else:
                try:
                    column_index, row_index = re.match(r"([a-z]+)([0-9]+)", command, re.I).groups()
                    if int(row_index) <= 0 or int(row_index) > self.max_rows or column_index not in headers:
                        return False
                except AttributeError:
                    pass
        return True

    def count_index(self, selected_item):
        """It return the index of selected_items.
        From a list, tuple and set."""
        iterCount = 0
        return_list = []
        if selected_item not in self.command:
            return None

        for item in self.command:
            iterCount += 1
            if item != selected_item:
                continue
            else:
                itemIndex = iterCount - 1
                itemCount = itemIndex + 1
                return_list.append(itemCount)

        return return_list

    def assign_error(self):
        """
        Preventing the assign error could
        happen due to user mistake and in
        coc code execution
        :return: bool
        """
        try:
            if self.command[0].isdigit():
                return False
            else:
                return True
        except IndexError:
            return True

    def validate_parentheses(self):
        """
        Validating parentheses it should
        be in pair
        :return: bool
        """
        if "(" in self.command and ")" not in self.command:
            return False
        return True
