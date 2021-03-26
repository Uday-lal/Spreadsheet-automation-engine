"""
--------------------------------------------------------->
Copyrights (c) to UR's tech.ltd 2021. All rights reserved
Author: Uday lal
company: UR's tech.ltd
--------------------------------------------------------->

~~~~~~~~~~~~~~~~~~~~~~~
Making the storage object to make wb data
some where at the center
"""
from kivy.storage.jsonstore import JsonStore
from datetime import datetime
import os
import json


class Storage(JsonStore):
    def __init__(self, **kwargs):
        super(Storage, self).__init__(**kwargs, filename="Propoint.json")
        self.filename = "Propoint.json"
        self.current_date = datetime.today().strftime("%d-%m-%Y")
        save_path = os.path.join(os.path.expanduser("~"), "AppData\\Roaming\\Propoint")

        try:
            os.mkdir(save_path)
        except FileExistsError:
            pass

        os.chdir(save_path)

    def save(self, wb_data, filename):
        """
        Saving the given data
        :param filename: Name of the workbook
        :param wb_data: Data need to be save
        :return: None
        """
        path, _filename = os.path.split(filename)
        self.put(key=_filename, path=path, date_of_modify=self.current_date, data=wb_data)

    def read_data(self):
        """
        Read the stored data
        :return: list
        """
        self.file = open(self.filename)
        data = json.load(self.file)
        for key in data:
            return data[key]["data"]

    def close_file(self):
        """
        Close the json file to pervert  ResourceWarning
        :return: None
        """
        self.file.close()
