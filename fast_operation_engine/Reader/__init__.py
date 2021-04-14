"""
--------------------------------------------------------->
Copyrights (c) to UR's tech.ltd 2021. All rights reserved
Author: Uday lal
company: UR's tech.ltd
--------------------------------------------------------->

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The reader object is going to read the codes
and make them in executable form
"""


class Reader:
    def __init__(self, codes, file_codes, current_obj):
        self.codes = codes
        self.file_codes = file_codes
        self.current_obj = current_obj
        self.data = {}

    def read(self):
        pass
