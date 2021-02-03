"""
--------------------------------------------------------->
Copyrights (c) to UR's tech.ltd 2021. All rights reserved
Author: Uday lal
company: UR's tech.ltd
--------------------------------------------------------->
"""
from openpyxl import load_workbook


class FileTypeException(Exception):
    def __init__(self, message):
        self.error_message = message


class Automate:
    def __init__(self, filename):
        self.filename = str(filename)
        if not self.filename.endswith(".xlsx"):
            raise FileTypeException(
                f"Excepting .xlsx file got {self.filename[self.filename.index('.'):len(self.filename)]}")

    def get_workbook_data(self):
        """
        Fetch the workbook data
        :return: dict
        """
        wb = load_workbook(self.filename)
        sheets = wb.sheetnames
        wb_data = {"sheets": sheets}

        for sheet in sheets:
            current_sheet = wb[sheet]
            max_cols = current_sheet.max_column
            max_rows = current_sheet.max_row
            rows_data = []
            sheet_data = {}
            rows = {}

            for row in range(1, max_rows + 1):
                for col in range(1, max_cols + 1):
                    cell_data = current_sheet.cell(row, col).value
                    if cell_data is None:
                        cell_data = ""

                    rows_data.append(cell_data)

                cols_data_copy = rows_data.copy()
                rows["row" + str(row)] = cols_data_copy
                sheet_data["rows"] = rows
                sheet_data["max_col"] = max_cols
                sheet_data["max_row"] = max_rows
                rows_data.clear()

            wb_data[sheet] = sheet_data

        return wb_data
