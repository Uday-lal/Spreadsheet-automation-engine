"""
--------------------------------------------------------->
Copyrights (c) to UR's tech.ltd 2021. All rights reserved
Author: Uday lal
company: UR's tech.ltd
--------------------------------------------------------->

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Saving workbook data with the help of
my MoF(Max of four) algorithm
"""
import threading


class SaveWorkbookData:
    def __init__(self, wb_obj, wb_data, updated_path, pointer_count=5):
        self.wb_data = wb_data
        self.wb_obj = wb_obj
        self.updated_path = updated_path
        self.pointer_count = pointer_count
        self.sheets = self.wb_data["sheets"]

    def save_data(self):
        for sheet in self.sheets:
            self.current_sheet = sheet
            self.current_sheet_data = self.wb_data[self.current_sheet]["rows"]
            self.max_cols = self.wb_data[self.current_sheet]["max_cols"]
            self.implement_mof()
        if self.updated_path is None:
            self.wb_obj.save(self.wb_data["file_path"])
        else:
            self.wb_obj.save(self.updated_path)

    def implement_mof(self):
        max_rows = len(self.wb_data[self.current_sheet]["rows"])
        index_slices = max_rows // self.pointer_count
        self.start_index = 1
        self.next_index = index_slices

        def save(data_to_save, sheet_data):
            for i, column in enumerate(sheet_data):
                master_cell = data_to_save[i].pop(0)
                for j, cell in enumerate(column):
                    try:
                        edited_cell_data = data_to_save[i][j]
                        if not edited_cell_data[1]:
                            cell.value = edited_cell_data[0]
                    except IndexError:
                        cell.value = ""
                data_to_save[i].insert(0, master_cell)

        for _ in range(self.pointer_count):
            data_slice = self.current_sheet_data[self.start_index:self.next_index + 1]
            sliced_sheet_data = self.slice_sheet_data()
            thread = threading.Thread(target=save, args=(data_slice, sliced_sheet_data))
            thread.start()
            self.start_index += index_slices
            self.next_index += index_slices

    def slice_sheet_data(self):
        rows = []
        for row_index in range(self.start_index, self.next_index + 1):
            rows_data = []
            for column_index in range(1, self.max_cols + 1):
                cell_data = self.wb_obj[self.current_sheet].cell(row_index, column_index)
                if cell_data is None:
                    cell_data = ""
                rows_data.append(cell_data)
            rows_data_copy = rows_data.copy()
            rows.append(rows_data_copy)
            rows_data.clear()

        return rows
