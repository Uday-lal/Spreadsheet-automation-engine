"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Defining the main executor object
"""
from ..apply_formulas import add, division, subtraction, multiplication
from generate_new_rc import GenerateNewRowsColumns
from str_replacement import StrReplacement
from mof_library.merge import Merge
import threading


class Executor:
    def __init__(self, sheet_data, data_for_execution):
        self.sheet_data = sheet_data
        self.data_for_execution = data_for_execution
        self.str_data_index = []
        self.root_key = list(self.data_for_execution.keys())[0]
        self.max_tolerance_point = 10
        self.total = 0

    def selection(self, coordinates, pointer_count=5):
        """
        Return selected data from sheet data.
        :param coordinates: Cell coordinate
        :param pointer_count: The number of threads is determine using that
        :return: list
        """
        selected_data = []
        self.max_rows = len(self.sheet_data)
        row_data_collection = {}
        max_tolerance_point = self.max_tolerance_point
        self.pointer_count = pointer_count
        str_data_index = self.str_data_index
        if len(coordinates) == 1:
            def implement_mof(data, thread_id, index_pair):
                row_data_slice = []
                iteration_pair = (0, len(data)) if thread_id != 0 else (1, len(data))
                p1, p2 = iteration_pair
                ip1, ip2 = index_pair
                for i in range(p1, p2):
                    ip1 += i
                    column_index = coordinates[0]
                    _selected_data = data[i][column_index][0]
                    is_master = data[i][column_index][1]
                    if type(_selected_data) is not str or is_master:
                        row_data_slice.append(_selected_data)
                    else:
                        str_data_index.append([(ip1 + 1, column_index, _selected_data)])
                        _selected_data = 0
                        if len(str_data_index) > max_tolerance_point:
                            row_data_slice.append("Exception")
                            break
                        row_data_slice.append(_selected_data)
                row_data_collection[thread_id] = row_data_slice

            index_slices = self.max_rows // self.pointer_count
            start_index = 0
            next_index = index_slices
            thread_id = 0
            for _ in range(self.pointer_count):
                index_pair = (start_index + 2, next_index + 2) if thread_id != 0 else (start_index, next_index + 2)
                p1, p2 = index_pair
                data_slice = self.sheet_data[p1:p2]
                thread = threading.Thread(target=implement_mof, args=(data_slice, thread_id, index_pair))
                thread.start()
                start_index += index_slices
                next_index += index_slices
                thread_id += 1
            thread_ids = sorted(list(row_data_collection.keys()))
            for thread_id in thread_ids:
                _row_data = row_data_collection[thread_id]
                if "Exception" in _row_data:
                    raise Exception("Sorry! We can't perform arithmetic on strings or words")
                selected_data += _row_data
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

    def marge(self, editor_screen):
        """
        Marge a the total sum on to the
        main sheet
        :return: list
        """
        try:
            total = self.total.tolist()
        except AttributeError:
            raise Exception("System dose not accept this input")
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
                merge = Merge(wb_data=self.sheet_data, total=total, root_key=self.root_key)
                merge.implement_mof()
                self.sheet_data, column_actual_values = merge.get_merged_data()
                if self.str_data_index:
                    str_replacement = StrReplacement(
                        wb_data=self.sheet_data,
                        str_index_data=self.str_data_index,
                        equal_to_index=self.root_key
                    )
                    self.sheet_data = str_replacement.perform_equal_to_replacement(
                        column_actual_values=column_actual_values,
                        total=total,
                        editor_screen=editor_screen
                    )
        else:
            generate_new_rc = GenerateNewRowsColumns(wb_data=self.sheet_data)
            generate_new_rc.generate()
            equal_to_index = len(self.sheet_data[0]) - 1
            merge = Merge(wb_data=self.sheet_data, total=total, root_key=equal_to_index)
            merge.implement_mof()
            if self.str_data_index:
                for str_data_index in self.str_data_index:
                    ci, ri, cell_value = str_data_index[0]
                    self.sheet_data[ci - 1][equal_to_index][0] = ""

        return self.sheet_data

    def get_data(self):
        """
        Yielding the data to save
        application from memory overflow
        :return: yield list
        """
        for i in range(1, len(self.sheet_data)):
            yield self.sheet_data[i], i
