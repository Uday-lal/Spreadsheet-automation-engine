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
from generate_new_rc import GenerateNewRowsColumns


class Executor:
    def __init__(self, sheet_data, data_for_execution):
        self.sheet_data = sheet_data
        self.data_for_execution = data_for_execution
        self.root_key = list(self.data_for_execution.keys())[0]
        self.total = 0

    def selection(self, coordinates):
        """
        Return selected data from sheet data.
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
        :return: None
        """
        data_for_operation = []
        for i, node in enumerate(self.data_for_execution[self.root_key]):
            operator = list(node.keys())[0]
            self.node_value = node[operator]
            if "is_universal" not in node:
                for coordinates in self.node_value:
                    data_for_operation.append(self.get_selected_data(coordinates))
                if len(data_for_operation) == 2:
                    first_value, next_value = data_for_operation
                else:
                    first_value, next_value = self.total, data_for_operation[0]
                self.perform_operation(
                    first_value=first_value,
                    next_value=next_value,
                    operation_type=operator
                )
            else:
                self.universal_node_operation = list(node.keys())[0]
                self.next_node_index = i + 1
                self.next_node = self.data_for_execution[self.root_key][self.next_node_index]
                self.perform_universal_operation()
            data_for_operation.clear()

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
        elif operation_type == "sub":
            self.total = subtraction(first_value, next_value)
        elif operation_type == "divide":
            self.total = division(first_value, next_value)
        elif operation_type == "multiply":
            self.total = multiplication(first_value, next_value)

    def perform_universal_operation(self):
        """
        Perform the defined operation if we
        found a universal operator
        :return: None
        """
        self.reset_total()
        self.data_for_execution[self.root_key].pop(self.next_node_index)
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

    def reset_total(self):
        """
        Reset the total back to its last value
        if we found a universal node.
        :return: None
        """
        last_node_data = self.get_selected_data(coordinates=self.node_value)
        self.total = subtraction(first_value=self.total, next_value=last_node_data)

    def marge(self):
        """
        Marge a the total sum on to the
        main sheet
        :return: list
        """
        try:
            total = self.total.tolist()
        except AttributeError:
            raise Exception("System dose not accept this input")
        i = 0
        _data = self.get_data()
        if self.root_key != "new":
            try:
                root_len = len(self.root_key)
            except TypeError:
                root_len = 1

            if root_len == 2:
                row_index, column_index = self.root_key
                cell_data = self.sheet_data[column_index][row_index]
                cell_data[0] = total if type(total) is not list else total[0]
                self.sheet_data[column_index][row_index] = cell_data
            else:
                while True:
                    try:
                        column_data = next(_data)
                        column_data[self.root_key][0] = total[i] if type(total) is list else total
                        i += 1
                    except StopIteration:
                        break
        else:
            generate_new_rc = GenerateNewRowsColumns(wb_data=self.sheet_data)
            generate_new_rc.generate()
            equal_to_index = len(self.sheet_data[0]) - 1
            while True:
                try:
                    row_data = next(_data)
                    row_data[equal_to_index][0] = total[i] if type(total) is list else total
                    i += 1
                except StopIteration:
                    break

        return self.sheet_data

    def get_data(self):
        """
        Yielding the data to save
        application from memory overflow
        :return: yield list
        """
        for i in range(1, len(self.sheet_data)):
            yield self.sheet_data[i]
