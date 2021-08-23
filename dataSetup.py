"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Cleaning the wb data and make it in correct shape.
"""
import string


class DataSetup:
    def __init__(self, data):
        self.sheet_data = data
        self.data = self.sheet_data["rows"]
        self.max_cols = self.sheet_data["max_cols"]
        try:
            self.is_cleaned = self.sheet_data["is_cleaned"]
        except KeyError:
            self.is_cleaned = False

    def get_clean_data(self):
        """
        Defining the process to clean the data.
        :return: dict
        """
        if not self.is_cleaned:
            self.insert_row_master()
            headers = self.get_headers()
            self.data.insert(0, headers)
            self.add_master_id()
            clean_data = self.data
            self.max_cols = len(clean_data[0])
            self.sheet_data["rows"] = clean_data
            self.sheet_data["max_cols"] = self.max_cols
            self.sheet_data["is_cleaned"] = True
            print(self.sheet_data)
        return self.sheet_data

    def get_headers(self):
        """
        Generate the header data based on the
        workbook data.
        :return: list
        """
        letters = [letter for letter in string.ascii_uppercase]
        letters.insert(0, "")

        if len(letters) < self.max_cols:
            max_len = len(letters)
            first_letter_i = round(self.max_cols / max_len)
            last_letter_i = self.max_cols - max_len

            for fli in range(first_letter_i):
                first_letter = letters[fli]
                for lli in range(last_letter_i):
                    last_letter = letters[lli]
                    letter = first_letter + last_letter
                    letters.append(letter)

            return letters[0:self.max_cols]

        else:
            return letters[0:self.max_cols]

    def insert_row_master(self):
        """
        Add the index on the wb_data
        :return: list
        """
        for index, row_data in enumerate(self.data, 1):
            row_data.insert(0, index)

        return self.data

    def add_master_id(self):
        """
        Defining a way to identify the index number and column header
        by constructing a data obj which is a list of three values such as ->

        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        [data, is_master, is_selected] =>
        ----------------------------------------
        data -> Data display to the dashboard
        is_master -> It is a boolean state
        is_selected -> It is also boolean state
        ---------------------------------------
        :return: list
        """
        for i, row_data in enumerate(self.data):
            for j, _data in enumerate(row_data):
                master_header = [_data, False, False]  # As documented above ↑
                if j == 0 or i == 0:
                    master_header[1] = True
                row_data[j] = master_header
