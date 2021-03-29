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

char_table = {
    'a': 'A',
    'b': 'B',
    'c': 'C',
    'd': 'D',
    'e': 'E',
    'f': 'F',
    'g': 'G',
    'h': 'H',
    'i': 'I',
    'j': 'J',
    'k': 'K',
    'l': 'L',
    'm': 'M',
    'n': 'N',
    'o': 'O',
    'p': 'P',
    'q': 'Q',
    'r': 'R',
    's': 'S',
    't': 'T',
    'u': 'U',
    'v': 'V',
    'w': 'W',
    'x': 'X',
    'y': 'Y',
    'z': 'Z'
}


class CoordinateOperationController:
    def __init__(self, headers, commands):
        self.commands = str(commands)
        self.headers = headers
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
        shape_input = self.shape_input()
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
                        shape_input[i + 1]
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

    def shape_input(self):
        """
        Make the input in perfect shape.

        -------------------------------------------
        sample_output: ["B", "*", "C"],
                       ["B1", "*", "C"] or
                       ["A1", "=", "B1", "*", "C"]
        -------------------------------------------
        :return: list
        """
        return_data = []

        for data in self.commands:
            if data != " ":
                if data in char_table.keys():
                    data = char_table[data]
                return_data.append(data)

        return self.clean_data(unclean_data=return_data)

    def clean_data(self, unclean_data):
        """
        Clean the unclean shape_data
        :return: list
        """
        clean_data = []

        for i, data in enumerate(unclean_data):
            if data.isalpha():
                current_index = i
                try:
                    while True:
                        current_index += 1
                        next_value = unclean_data[current_index]
                        if next_value.isdigit():
                            data += next_value
                        else:
                            break
                except IndexError:
                    pass

            if data.isdigit() and i != 0:
                if not unclean_data[i - 1] in self.operators.keys():
                    data = None
            clean_data.append(data)

        clean_data = list(filter(None, clean_data))

        return clean_data
