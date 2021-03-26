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
from storage import Storage

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
    def __init__(self):
        self.storage = Storage()
        self.operations = {  # Defining the possible operations with several commands
            "+": "add",
            "-": "sub",
            "/": "divide",
            "*": "multiply"
        }

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
        headers = self.storage.read_data()["rows"][0]
        self.storage.close_file()
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

    def selector(self, inputs):
        """
        Select cell, rows and column on to the
        given data
        :return: list
        """
        selected_data = []
        self.inputs = inputs
        clean_input = self.clean_input()
        print("clean_input: ", clean_input)
        indexes = self.data_index(sample_input=clean_input)
        wb_data = self.storage.read_data()["rows"]
        c1, c2 = indexes

        def direct_selector(index):
            data = self.gen(data=wb_data)
            while True:
                try:
                    selected_data.append(next(data)[index][0])
                except StopIteration:
                    break

        def dual_selection(coordinate):
            cc, rc = coordinate  # cc => (Column coordinate), rc => (Row coordinate)
            selected_data.append(wb_data[cc][rc][0])

        if type(c1) is tuple or type(c2) is tuple:
            for index in indexes:
                if index is tuple:
                    dual_selection(coordinate=index)
                elif index is tuple:
                    dual_selection(coordinate=index)
                else:
                    direct_selector(index=index)

        else:
            for index in indexes:
                direct_selector(index=index)

        return selected_data

    @staticmethod
    def gen(data):
        """
        Generator method which help us to iterate
        as fast as possible
        :param data: Data on which we need to iterate
        :return: generator
        """
        for i in range(len(data)):
            yield data[i]
