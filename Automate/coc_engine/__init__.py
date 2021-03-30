"""
--------------------------------------------------------->
Copyrights (c) to UR's tech.ltd 2021. All rights reserved
Author: Uday lal
company: UR's tech.ltd
--------------------------------------------------------->

~~~~~~~~~~~~~~~~~~~~~~~
COC(Coordinate Operation Controller) is type engine which is
responsible for handle all the inputs coming from input box
to select cells to perform mathematical logic
"""
import re
from .clean_command import CleanCommand


class CoordinateOperationController:
    def __init__(self, headers, commands):
        self.commands = str(commands)
        self.headers = headers
        self.clean_command = CleanCommand(commands=self.commands)
        self.operators = {  # Defining the possible operators with several commands
            "+": "add",
            "-": "sub",
            "/": "divide",
            "*": "multiply",
            "=": "equal_to"
        }

    def execute(self):
        """
        Execute the command that are
        given.
        :return: dict
        """
        data_for_execution = {}
        shape_input = self.clean_command.shape_input()
        root_key = "new"
        operator_coming_times = 0
        if "=" in shape_input:
            root_key = self.data_index(command=[shape_input[0]])[0]
            shape_input = shape_input[2:len(shape_input)]
        data_for_execution[root_key] = []

        for i, command in enumerate(shape_input):
            operator = self.operators[command] if command in self.operators else None

            if operator is not None:
                operator_coming_times += 1
                node = {}
                if operator_coming_times == 1:
                    last_value, next_value = self.data_index([shape_input[i - 1]])[0], self.data_index(
                        [shape_input[i + 1]])[0]
                    node[operator] = (last_value, next_value)
                    data_for_execution[root_key].append(node)
                else:
                    next_value = self.data_index(command=[shape_input[i + 1]])[0] if not shape_input[
                        i + 1].isdigit() else \
                        int(shape_input[i + 1])
                    node[operator] = next_value
                    data_for_execution[root_key].append(node)

        return data_for_execution

    def data_index(self, command):
        """
        Returns the index of each command
        or input presented in the headers

        --------------------------------
        sample input: ["B", "*", "C"]
        --------------------------------
        :param command: Input data base on which it going to return some value
        :return: list
        """
        headers = self.headers

        return_data = []

        for value in command:
            for header in headers:
                if len(value) == 1:
                    if value in header:
                        return_data.append(headers.index(header))
                else:
                    row_index, column_index = re.match(r"([a-z]+)([0-9]+)", value, re.I).groups()
                    if row_index in header:
                        return_data.append((headers.index(header), int(column_index)))

        return return_data