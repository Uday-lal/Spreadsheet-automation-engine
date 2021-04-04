"""
--------------------------------------------------------->
Copyrights (c) to UR's tech.ltd 2021. All rights reserved
Author: Uday lal
company: UR's tech.ltd
--------------------------------------------------------->

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Generate new rows and columns
"""
from dataSetup import DataSetup


class GenerateNewRowsColumns:
    def __init__(self, wb_data):
        self.wb_data = wb_data
        self.headers = self.wb_data[0]

    def generate(self):
        for row_data in self.wb_data:
            row_data.append("")

        max_cols = len(self.wb_data[0])
        headers = DataSetup(data=self.wb_data, max_cols=max_cols).get_headers()
        self.wb_data[0] = headers
        return self.wb_data
