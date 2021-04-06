"""
--------------------------------------------------------->
Copyrights (c) to UR's tech.ltd 2021. All rights reserved
Author: Uday lal
company: UR's tech.ltd
--------------------------------------------------------->

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Cleaning the users commands
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


class CleanCommand:
    def __init__(self, commands):
        self.commands = commands
        self.operators = {  # Defining the possible operators with several commands
            "+": "add",
            "-": "sub",
            "/": "divide",
            "*": "multiply",
            "=": "equal_to"
        }

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
        # insert_float = lambda current_value, last_value, next_value: last_value + current_value + next_value
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

            if data == ".":
                pass

            if data.isdigit() and i != 0:
                current_index = i
                while True:
                    current_index += 1
                    next_value = unclean_data[current_index]
                    if next_value.isdigit() or next_value == ".":
                        data += next_value
                    else:
                        break
                if not unclean_data[i - 1] in self.operators.keys():
                    data = None
            clean_data.append(data)

        clean_data = list(filter(None, clean_data))
        if "." in clean_data:
            dot_index = clean_data.index(".")
            clean_data.pop(dot_index)

        return clean_data
