"""
--------------------------------------------------------->
Copyrights (c) to UR's tech.ltd. All rights reserved
Author: Uday lal
company: UR's tech.ltd
--------------------------------------------------------->
"""

from kivymd.app import MDApp
from kivy.lang import Builder
from manager import Manger


class Propoint(MDApp):
    def build(self):
        Builder.load_file("main.kv")
        manager = Manger()
        return manager


if __name__ == "__main__":
    Propoint().run()
