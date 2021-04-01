"""
--------------------------------------------------------->
Copyrights (c) to UR's tech.ltd 2021. All rights reserved
Author: Uday lal
company: UR's tech.ltd
--------------------------------------------------------->

~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Defining the main executor object
"""


class Executor:
    def __init__(self, sheet_data, data_for_execution):
        self.sheet_data = sheet_data
        self.data_for_execution = data_for_execution

    def selection(self, coordinates):
        selected_data = []
        if len(coordinates) == 1:
            for row_data in self.sheet_data:
                column_index = coordinates
                selected_data.append(row_data[column_index][0])
        else:
            column_index, row_index = coordinates
            selected_data.append(self.sheet_data[row_index][column_index][0])

        return selected_data

    def execute(self):
        """
        Execute the given command
        :return: list
        """
        pass
