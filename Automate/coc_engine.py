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
        shaped_input = self.shape_input()

    def data_index(self, sample_input):
        """
        Understanding the input and based on that
        raise several actions

        --------------------------------
        sample input: ["B", "*", "C"]
        --------------------------------
        :param sample_input: Input data base on which it going to return some value
        :return: list
        """
        headers = self.headers["rows"][0]

        return_data = []

        for value in sample_input:
            for header in headers:
                if len(value) < 2:
                    if value in header:
                        return_data.append(headers.index(header))
                else:
                    row_index, column_index = value
                    if row_index in header:
                        return_data.append((headers.index(header), column_index))

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
