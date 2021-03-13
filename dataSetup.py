"""
--------------------------------------------------------->
Copyrights (c) to UR's tech.ltd 2021. All rights reserved
Author: Uday lal
company: UR's tech.ltd
--------------------------------------------------------->

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Cleaning the wb data and make it in correct shape.
"""
import string


class DataSetup:
    def __init__(self, data):
        self.sheet_data = data
        self.data = self.sheet_data["rows"]
        self.max_cols = self.sheet_data["max_cols"]

    def get_clean_data(self):
        """
        Defining the process to clean the data.
        :return: dict
        """
        clean_data = self.insert_row_master()
        self.max_cols = len(clean_data[0])
        headers = self.get_headers()
        clean_data.insert(0, headers)
        self.sheet_data["rows"] = clean_data
        self.sheet_data["max_cols"] = self.max_cols
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
        index = 0
        for row_data in self.data:
            index += 1
            row_data.insert(0, index)

        return self.data
