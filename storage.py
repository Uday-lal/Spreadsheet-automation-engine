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
import os
import json


class Storage(JsonStore):
    def __init__(self, **kwargs):
        super(Storage, self).__init__(**kwargs, filename="Propoint.json")
        self.filename = "Propoint.json"
        save_path = os.path.join(os.path.expanduser("~"), "AppData\\Roaming")
        if "Propoint" in os.listdir(save_path):
            self.is_first_store = False
        else:
            self.is_first_store = True

        save_path = os.path.join(save_path, "Propoint")
        try:
            os.mkdir(save_path)
        except FileExistsError:
            pass
        os.chdir(save_path)

    def save(self, data):
        file = open(self.filename, "w")
        json.dump(data, file)
        file.close()

    def read(self, filename):
        file = open(self.filename, "r")
        data = json.load(file)
        return data[filename]

    def read_all(self):
        file = open(self.filename, "r")
        return json.load(file)

    def delete_history(self, filename):
        save_data = self.read_all()
        del save_data[filename]
        self.save(data=save_data)
