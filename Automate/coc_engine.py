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
    def __init__(self, data, inputs):
        self.inputs = str(inputs)
        self.data = data
        self.operations = {  # Defining the possible operations with several commands
            "+": "add",
            "-": "sub",
            "/": "divide",
            "*": "multiply"
        }

    def input_decoder(self):
        """
        Understanding the input and based on that
        raise several actions

        --------------------------------
        sample input: ["b", "*", "c"]
        --------------------------------
        :return: tuple
        """
        value1, operation, value2 = self.clean_input()
        operation = self.operations[operation]
        value1_index = self.data.index(value1)
        value2_index = self.data.index(value2)
        return value1_index, operation, value2_index

    def clean_input(self):
        """
        Cleaning the input and make it
        in perfect shape
        :return: list
        """
        return_data = []

        for data in self.inputs:
            if data != " ":
                if data in char_table.keys():
                    data = char_table[data]
                return_data.append(data)

        return return_data
