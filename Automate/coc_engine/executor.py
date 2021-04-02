"""
--------------------------------------------------------->
Copyrights (c) to UR's tech.ltd 2021. All rights reserved
Author: Uday lal
company: UR's tech.ltd
--------------------------------------------------------->

~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Defining the main executor object
"""
from ..apply_formulas import add, division, subtraction, multiplication


class Executor:
    def __init__(self, sheet_data, data_for_execution):
        self.sheet_data = sheet_data
        self.data_for_execution = data_for_execution
        self.total = 0

    def selection(self, coordinates):
        """
        Return selected data from sheet
        data.
        :param coordinates: Cell coordinate
        :return: list
        """
        selected_data = []
        if len(coordinates) == 1:
            for i in range(1, len(self.sheet_data)):
                column_index = coordinates[0]
                selected_data.append(self.sheet_data[i][column_index][0])
        else:
            column_index, row_index = coordinates
            selected_data.append(self.sheet_data[row_index][column_index][0])

        return selected_data

    def execute(self):
        """
        Execute the given command
        :return: list
        """
        print(self.data_for_execution)
        root_key = list(self.data_for_execution.keys())[0]
        operation_data = []
        for i, node in enumerate(self.data_for_execution[root_key]):
            operator = list(node.keys())[0]
            node_value = node[operator]
            if "is_universal" not in node:
                for coordinate in node_value:
                    operation_data.append(self.get_selected_data(coordinates=coordinate))
                if len(operation_data) == 2:
                    first_value, next_value = operation_data
                else:
                    first_value, next_value = self.total, operation_data[0]
                self.perform_operation(operation_type=operator, first_value=first_value, next_value=next_value)
            else:
                self.universal_node_operation = list(node.keys())[0]
                self.next_node = self.data_for_execution[root_key][i + 1]
                self.perform_universal_operation()

        return self.total

    def get_selected_data(self, coordinates):
        """
        Defining the rules of selection
        :param coordinates: cells coordinates
        :return: list
        """
        if type(coordinates) is tuple:
            first_index_value, next_index_value = coordinates
            if first_index_value != "isdigit":
                return self.selection(coordinates=(first_index_value, next_index_value))
            else:
                return next_index_value
        else:
            return self.selection(coordinates=[coordinates])

    def perform_operation(self, first_value, next_value, operation_type):
        """
        Perform mathematical operation
        :param operation_type: type of operation
        :param first_value:
        :param next_value:
        :return: None
        """
        if operation_type == "add":
            self.total = add(first_value, next_value)
            print(self.total)
        if operation_type == "sub":
            self.total = subtraction(first_value, next_value)
        if operation_type == "divide":
            self.total = division(first_value, next_value)
        if operation_type == "multiply":
            self.total = multiplication(first_value, next_value)

    def perform_universal_operation(self):
        """
        Perform the defined operation if we
        found a universal operator
        :return: None
        """
        next_node_operator = list(self.next_node.keys())[0]
        next_node_value = self.next_node[next_node_operator]
        next_node_operation_data = []
        for coordinate in next_node_value:
            next_node_operation_data.append(self.get_selected_data(coordinates=coordinate))

        first_value, next_value = next_node_operation_data

        if next_node_operator == "multiply":
            multiply_ans = multiplication(first_value, next_value)
            self.perform_operation(
                first_value=self.total,
                next_value=multiply_ans,
                operation_type=self.universal_node_operation
            )
        if next_node_operator == "divide":
            division_ans = division(first_value, next_value)
            self.perform_operation(
                first_value=self.total,
                next_value=division_ans,
                operation_type=self.universal_node_operation
            )
