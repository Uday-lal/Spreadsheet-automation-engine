"""
--------------------------------------------------------->
Copyrights (c) to UR's tech.ltd 2021. All rights reserved
Author: Uday lal
company: UR's tech.ltd
--------------------------------------------------------->

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Generate new rows and columns
"""
import string


class GenerateNewRowsColumns:
    def __init__(self, wb_data):
        self.wb_data = wb_data
        self.headers = self.wb_data[0]
        self.max_cols = len(self.headers)

    def generate(self):
        for row_data in self.wb_data:
            row_data.append(["", False, False])

        self.max_cols = len(self.wb_data[0])
        headers = self.get_headers()
        self.wb_data[0] = headers
        return self.wb_data

    def get_headers(self):
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

            self.selected_letter_part = letters[0:self.max_cols]
            self.insert_master_identifier()
            return self.selected_letter_part

        else:
            self.selected_letter_part = letters[0:self.max_cols]
            self.insert_master_identifier()
            return self.selected_letter_part

    def insert_master_identifier(self):
        """
        Inserting master identifier
        or the booleans
        :return: None
        """
        for i, header in enumerate(self.selected_letter_part):
            self.selected_letter_part[i] = [header, True, False]
