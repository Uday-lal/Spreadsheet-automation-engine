"""
--------------------------------------------------------->
Copyrights (c) to UR's tech.ltd 2021. All rights reserved
Author: Uday lal
company: UR's tech.ltd
--------------------------------------------------------->

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Apply selection using MoF algorithm
"""
import threading


class ApplySelection:
    def __init__(self, data, pointer_count=5):
        self.data = data
        self.pointer_count = pointer_count
        self.row_data_collection = {}

    def master_selection(self, data, thread_id):
        """
        Update the data dict on the master selection
        :param data: Sliced data
        :param thread_id:
        :return: None
        """
        _data = self.get_data(data)
        processing_data = []
        while True:
            try:
                cell_data = next(_data)[self.column_index]
                cell_data[2] = True
                processing_data.append(cell_data)
            except StopIteration:
                self.row_data_collection[thread_id] = processing_data
                break

    @staticmethod
    def get_data(data):
        """
        Iterate through the data
        as by yielding it
        :return: generator object
        """
        for row_data in data:
            yield row_data

    @staticmethod
    def apply_selection(cell):
        """
        Reverse the state of is_selected boolean
        :param cell: Instance of cell object
        :return: None
        """
        cell.is_selected = True
        return cell.text

    def master_column_selection(self, data, thread_id):
        _data = self.get_data(data)
        processing_data = []

        while True:
            try:
                cell_data = next(_data)
                cell_data[2] = True
                processing_data.append(cell_data)
            except StopIteration:
                self.row_data_collection[thread_id] = processing_data
                break

    def unselect(self, data, thread_id):
        """
        Defining the way to unselect
        the selected cell.
        :return: None
        """
        _data = self.get_data(data)
        processing_data = []
        while True:
            try:
                cells_data = next(_data)
                for cell_data in cells_data:
                    cell_data[2] = False
                processing_data.append(cells_data)
            except StopIteration:
                self.row_data_collection[thread_id] = processing_data
                break

    @staticmethod
    def start_mof(target_func, *args):
        """
        Start mof algorithm for this object
        :param target_func: The target function for which we want to
        start mof
        :return: None
        """
        thread = threading.Thread(target=target_func, args=args)
        thread.start()

    def implement_mof(self, cell):
        """
        Select the data using MoF algorithm
        :param cell: Cell object
        :return: None
        """
        self.column_index = cell.column_index
        self.row_index = cell.row_index
        self.unselect_mode = False
        _data = self.data if not cell.text.isdigit() else self.data[self.row_index]
        max_rows = len(_data)
        index_slices = max_rows // self.pointer_count
        start_index = 0
        next_index = index_slices
        thread_id = 0

        if cell.text != "":
            for _ in range(self.pointer_count):
                data_slice = _data[start_index + 2:next_index + 2] if thread_id != 0 else \
                    _data[start_index:next_index + 2]
                self.start_mof(self.master_selection, data_slice, thread_id) if not cell.text.isdigit() else \
                    self.start_mof(self.master_column_selection, data_slice, thread_id)
                start_index += index_slices
                next_index += index_slices
                thread_id += 1

    def merge(self, is_row_merging):
        thread_ids = sorted(list(self.row_data_collection.keys()))
        merged_data = []
        for thread_id in thread_ids:
            _row_data = self.row_data_collection[thread_id]
            if not is_row_merging or self.unselect_mode:
                merged_data += _row_data
            else:
                merged_data += _row_data
                self.data[self.row_index] = merged_data
        return self.data

    def implement_mof_for_unselect(self):
        self.unselect_mode = True
        _data = self.data
        max_rows = len(_data)
        index_slices = max_rows // self.pointer_count
        start_index = 0
        next_index = index_slices
        thread_id = 0

        for _ in range(self.pointer_count):
            data_slice = _data[start_index + 2:next_index + 2] if thread_id != 0 else _data[start_index:next_index + 2]
            self.start_mof(self.unselect, data_slice, thread_id)
            start_index += index_slices
            next_index += index_slices
            thread_id += 1
