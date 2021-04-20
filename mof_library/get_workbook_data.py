"""
--------------------------------------------------------->
Copyrights (c) to UR's tech.ltd 2021. All rights reserved
Author: Uday lal
company: UR's tech.ltd
--------------------------------------------------------->

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Getting workbook data with the help of
my MoF(Max of four) algorithm
"""
import threading


class GetWbData:
    def __init__(self, wb_obj, filename, pointer_count=5):
        self.wb_obj = wb_obj
        self.sheets = self.wb_obj.sheetnames
        self.wb_data = {"file_path": filename, "sheets": self.sheets}
        self.pointer_count = pointer_count

    def get_data(self):
        for sheet in self.sheets:
            sheet_data = {}
            self.current_sheet = self.wb_obj[sheet]
            rows = self.start_iteration()
            max_cols = self.current_sheet.max_column
            max_rows = self.current_sheet.max_row
            sheet_data["rows"] = rows
            sheet_data["max_cols"] = max_cols + 1
            sheet_data["max_row"] = max_rows
            self.wb_data[sheet] = sheet_data
        return self.wb_data

    def start_iteration(self):
        current_sheet = self.current_sheet
        max_cols = current_sheet.max_column
        max_rows = current_sheet.max_row
        index_slices = max_rows // self.pointer_count
        rows = []
        rows_data = []

        def start(slice_index):
            """
            Starting the loop to perform
            mof
            :param slice_index: Index to slice the iterable obj
            :return: None
            """
            x, y = slice_index
            for row in range(x, y + 1):
                for col in range(1, max_cols + 1):
                    cell_data = current_sheet.cell(row, col).value
                    if cell_data is None:
                        cell_data = ""

                    rows_data.append(cell_data)

                rows_data_copy = rows_data.copy()
                rows.append(rows_data_copy)
                rows_data.clear()

        start_index = 1
        next_index = index_slices

        for i in range(self.pointer_count):
            index_pair = (start_index, next_index) if i != (self.pointer_count - 1) else (start_index, next_index + 1)
            thread = threading.Thread(target=start, args=(index_pair,))
            thread.start()
            start_index += index_slices
            next_index += index_slices

        return rows
