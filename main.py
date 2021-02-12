"""
--------------------------------------------------------->
Copyrights (c) to UR's tech.ltd 2021. All rights reserved
Author: Uday lal
company: UR's tech.ltd
--------------------------------------------------------->
"""

from kivymd.app import MDApp
from kivy.lang import Builder
from manager import Manager


class Propoint(MDApp):
    def build(self):
        """
        Strat building the app
        :return: Root widget
        """
        Builder.load_file("main.kv")
        root = Manager()
        return root


if __name__ == "__main__":
    Propoint().run()
