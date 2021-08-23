"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Defining the way of merging using mof algorithm
"""
import threading


class Merge:
    def __init__(self, wb_data, total, root_key):
        self.wb_data = wb_data
        self.total = total
        self.root_key = root_key
        self.max_rows = len(self.wb_data)
        self.actual_column_data_collection = {}
        self.iter_time = 0

    def get_data(self, data):
        for i in range(len(data)):
            self.iter_time += 1
            yield data[i], self.iter_time

    def merge(self, data, thread_id, index_pair):
        _data = self.get_data(data=data)
        column_actual_values = []
        i = 0
        p1, p2 = index_pair
        total = self.total[p1:p2] if type(self.total) is list else self.total

        while True:
            try:
                try:
                    column_data = next(_data)
                    actual_value = column_data[0][self.root_key][0]
                    if type(actual_value) is str and type(total) is list:
                        column_actual_values.append((column_data[1], self.root_key, actual_value))
                    column_data[0][self.root_key][0] = total[i] if type(total) is list else total
                    i += 1
                except IndexError:
                    pass
            except StopIteration:
                self.actual_column_data_collection[thread_id] = column_actual_values
                break

    def implement_mof(self, pointer_count=5):
        headers = self.wb_data.pop(0)
        self.max_rows = len(self.wb_data)
        index_slices = self.max_rows // pointer_count
        start_index = 0
        next_index = index_slices
        thread_id = 0

        for _ in range(pointer_count):
            index_pair = (start_index + 2, next_index + 2) if thread_id != 0 else (start_index, next_index + 2)
            p1, p2 = index_pair
            data_slice = self.wb_data[p1:p2]
            thread = threading.Thread(target=self.merge, args=(data_slice, thread_id, index_pair))
            thread.start()
            start_index += index_slices
            next_index += index_slices
            thread_id += 1
        self.wb_data.insert(0, headers)

    def merge_column_data(self):
        thread_ids = sorted(list(self.actual_column_data_collection.keys()))
        column_data = []
        for thread_id in thread_ids:
            column_data += self.actual_column_data_collection[thread_id]
        return column_data

    def get_merged_data(self):
        column_data = self.merge_column_data()
        return self.wb_data, column_data
