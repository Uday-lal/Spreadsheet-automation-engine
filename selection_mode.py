"""
--------------------------------------------------------->
Copyrights (c) to UR's tech.ltd 2021. All rights reserved
Author: Uday lal
company: UR's tech.ltd
--------------------------------------------------------->

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Defining the rules of selection mode
"""
from Automate.apply_formulas import add, multiplication, division, subtraction
from generate_new_rc import GenerateNewRowsColumns
from Automate.coc_engine.clean_command import CleanCommand
import re


class SelectionMode:
    def __init__(self, max_rc, selected_data, operation_type, equal_to, wb_data):
        self.selected_data = selected_data
        self.max_cols = max_rc[0] + 1
        self.max_rows = max_rc[1] + 1
        self.clean_selected_data = []
        self.total = 0
        self.equal_to = equal_to
        self.wb_data = wb_data
        self.operation_type = operation_type
        self.headers = self.wb_data[0]
        self.clean_data()

    def execute(self):
        if self.operation_type == "Sort":
            self.sort()
        elif self.operation_type == "Reverse":
            self.reverse()
        elif self.operation_type == "Delete":
            self.delete()
        elif self.operation_type == "Apply formulas/add":
            self.add()
        elif self.operation_type == "Apply formulas/multiply":
            self.multiplication()
        elif self.operation_type == "Apply formulas/divide":
            self.division()
        elif self.operation_type == "Apply formulas/sub":
            self.subtraction()

    def add(self):
        for i, data in enumerate(self.clean_selected_data):
            if i == 0:
                first_value, next_value = data, self.clean_selected_data[i + 1]
                self.total = add(first_value=first_value, next_value=next_value)
                if len(self.clean_selected_data) == 2:
                    break
            else:
                first_value, next_value = self.total, data
                self.total = add(first_value=first_value, next_value=next_value)
        return self.total

    def multiplication(self):
        for i, data in enumerate(self.clean_selected_data):
            if i == 0:
                first_value, next_value = data, self.clean_selected_data[i + 1]
                self.total = multiplication(first_value=first_value, next_value=next_value)
                if len(self.clean_selected_data) == 2:
                    break
            else:
                first_value, next_value = self.total, data
                self.total = multiplication(first_value=first_value, next_value=next_value)
        return self.total

    def division(self):
        for i, data in enumerate(self.clean_selected_data):
            if i == 0:
                first_value, next_value = data, self.clean_selected_data[i + 1]
                self.total = division(first_value=first_value, next_value=next_value)
                if len(self.clean_selected_data) == 2:
                    break
            else:
                first_value, next_value = self.total, data
                self.total = division(first_value=first_value, next_value=next_value)
        return self.total

    def subtraction(self):
        for i, data in enumerate(self.clean_selected_data):
            if i == 0:
                first_value, next_value = data, self.clean_selected_data[i + 1]
                self.total = subtraction(first_value=first_value, next_value=next_value)
                if len(self.clean_selected_data) == 2:
                    break
            else:
                first_value, next_value = self.total, data
                self.total = subtraction(first_value=first_value, next_value=next_value)
        return self.total

    def sort(self):
        pass

    def reverse(self):
        pass

    def delete(self):
        pass

    def clean_data(self):
        max_iter_time = len(self.selected_data) // self.max_cols
        iter_time = 0
        selected_column_data = []
        while iter_time != max_iter_time:
            iter_time += 1
            for i in range(1, self.max_cols):
                selected_column_data.append(self.selected_data[i][0])
            self.clean_selected_data.append(selected_column_data.copy())
            del self.selected_data[0:self.max_cols]
            selected_column_data.clear()

    def marge(self):
        total = self.total.tolist()
        if self.equal_to == "new":
            generate_new_rc = GenerateNewRowsColumns(wb_data=self.wb_data)
            generate_new_rc.generate()
            equal_to_index = len(self.wb_data[0]) - 1
            _data = self.get_data()
            i = 0
            while True:
                try:
                    row_data = next(_data)
                    row_data[equal_to_index][0] = total[i] if type(total) is list else total
                    i += 1
                except StopIteration:
                    break
        else:
            shape_input = CleanCommand(commands=self.equal_to).shape_input()
            equal_to_index = self.get_data_index(equal_to_value=shape_input)[0]
            if type(equal_to_index) is int:
                _data = self.get_data()
                i = 0
                while True:
                    try:
                        row_data = next(_data)
                        row_data[equal_to_index][0] = total[i] if type(total) is list else total
                        i += 1
                    except StopIteration:
                        break
            else:
                row_index, column_index = equal_to_index
                self.wb_data[column_index][row_index][0] = total
        return self.wb_data

    def get_data_index(self, equal_to_value):
        headers = self.headers

        return_data = []

        for value in equal_to_value:
            if value.isdigit():
                return_data.append(("isdigit", int(value)))
            for header in headers:
                if len(value) == 1:
                    if value in header:
                        return_data.append(headers.index(header))
                else:
                    row_index, column_index = re.match(r"([a-z]+)([0-9]+)", value, re.I).groups()
                    if row_index in header:
                        return_data.append((headers.index(header), int(column_index)))

        return return_data

    def get_data(self):
        """
        Yielding the data to save
        application from memory overflow
        :return: yield list
        """
        for i in range(1, len(self.wb_data)):
            yield self.wb_data[i]