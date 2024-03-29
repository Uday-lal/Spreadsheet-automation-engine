"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Starting the building the application.
"""

from kivymd.app import MDApp
from kivy.lang import Builder
from manager import Manager


class Propoint(MDApp):
    title = "Propoint"

    def build(self):
        """
        Start building the app
        :return: Root widget
        """
        Builder.load_file("main.kv")
        root = Manager()
        return root


if __name__ == "__main__":
    Propoint().run()
