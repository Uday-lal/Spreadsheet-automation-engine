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

    def master_selection(self, column_index):
        """
        Update the data dict on the master selection
        :param column_index: Column index of the cell
        :return: None
        """
        _data = self.get_data()

        while True:
            try:
                cell_data = next(_data)[column_index]
                cell_data[2] = True
                processing_data.append(cell_data)
            except StopIteration:
                return processing_data

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
