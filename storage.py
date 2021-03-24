"""
--------------------------------------------------------->
Copyrights (c) to UR's tech.ltd 2021. All rights reserved
Author: Uday lal
company: UR's tech.ltd
--------------------------------------------------------->

~~~~~~~~~~~~~~~~~~~~~~~
Making the storage object and and enabling the
live storing the feature.
"""
from kivy.storage.jsonstore import JsonStore
from datetime import datetime
import os


class Storage(JsonStore):
    def __init__(self, **kwargs):
        super(Storage, self).__init__(**kwargs)
        try:
            self.filename = "Propoint.json"
            self.current_date = datetime.today().strftime("%d-%m-%Y")
            save_path = os.path.join(os.path.expanduser("~"), "AppData\\Roaming\\Propoint")
            os.mkdir(save_path)
            os.chdir(save_path)
        except FileExistsError:
            pass

    def save(self, wb_data):
        """
        Saving the given data
        :param wb_data: Data need to be save
        :return: None
        """
        self.put(key=wb_data["filename"], date_of_modify=self.current_date, data=wb_data["data"])

    def read_data(self, filename):
        """
        Read the stored data
        :param filename: Name of the workbook
        :return: list
        """
        return self.get(key=filename)["data"]
