"""
--------------------------------------------------------->
Copyrights (c) to UR's tech.ltd 2021. All rights reserved
Author: Uday lal
company: UR's tech.ltd
--------------------------------------------------------->

~~~~~~~~~~~~~~~~~~~~~~~~~~~
Making the selection making object which is
responsible for making selections and provide selected data
"""

processing_data = []


class ApplySelection:
    def __init__(self, data):
        self.data = data

    def master_selection(self, cell):
        """
        Update the data dict on the master selection
        :param cell: Cell object
        :return: None
        """
        self.column_index = cell.column_index
        self.row_index = cell.row_index
        if not cell.text.isdigit():
            _data = self.get_data()

            while True:
                try:
                    cell_data = next(_data)[self.column_index]
                    cell_data[2] = True
                    processing_data.append(cell_data)
                except StopIteration:
                    return processing_data
        else:
            self.master_column_selection()

    def get_data(self):
        """
        Iterate through the data
        as by yielding it
        :return: generator object
        """
        for data in self.data:
            yield data

    @staticmethod
    def apply_selection(cell):
        """
        Reverse the state of is_selected boolean
        :param cell: Instance of cell object
        :return: None
        """
        cell.is_selected = True

    def master_column_selection(self):
        self.data = self.data[self.row_index]
        _data = self.get_data()

        while True:
            try:
                cell_data = next(_data)
                cell_data[2] = True
                processing_data.append(cell_data)
            except StopIteration:
                return processing_data
