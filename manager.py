"""
--------------------------------------------------------->
Copyrights (c) to UR's tech.ltd 2021. All rights reserved
Author: Uday lal
company: UR's tech.ltd
--------------------------------------------------------->
"""
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager

from screen import HomeScreen, TutorialScreen, EditorScreen
from dashboard import DashBoard
from dataSetup import DataSetup
from kivy.properties import StringProperty
from Automate import Automate
from storage import Storage
import os


class Manager(ScreenManager):
    current_sheet = StringProperty()

    def __init__(self, **kwargs):
        super(Manager, self).__init__(**kwargs)
        self.home_screen = HomeScreen(name="home_screen")
        self.tutorial_screen = TutorialScreen(name="tutorial_screen")
        self.editor_screen = EditorScreen(name="editor_screen")
        self.add_widget(self.home_screen)
        self.add_widget(self.tutorial_screen)
        self.add_widget(self.editor_screen)

    def screen_transition_home(self):
        """
        Define screen transition home
        :return: None
        """
        if self.current_screen.name != "home_screen":
            self.transition.direction = "down"
            self.current = "home_screen"

    def screen_transition_tutorial(self):
        """
        Define screen transition tutorial
        :return: None
        """
        if self.current_screen.name != "tutorial_screen":
            self.transition.direction = "up"
            self.current = "tutorial_screen"

    def empty_home_screen(self):
        """
        Define home screen if user history is empty
        :return: None
        """
        anchor_layout = AnchorLayout()
        image = Image(source="assets/images/empty.png", size_hint_x=None,
                      size_hint_y=None, width=300, height=300)
        anchor_layout.add_widget(image)
        self.home_screen.add_widget(anchor_layout)

    def render_wb_data(self, render_data):
        """
        Define the way to render the wb data
        :return: None
        """
        self.sheets = render_data["sheets"]  # Making the reference to dropdown items.
        self.render_data = render_data
        sheet_data = self.render_data[self.sheets[0]]
        self.current_sheet = self.sheets[0]
        clean_data = self.clean_data(data=sheet_data)
        self.render_data[self.sheets[0]]["rows"] = clean_data["rows"]
        row_data = clean_data["rows"]
        max_cols = clean_data["max_cols"]
        self.dash_board = DashBoard()
        self.editor_screen.ids.dashboard = self.dash_board
        self.dash_board.data = row_data
        self.dash_board.max_cols = max_cols
        self.dash_board.render_data(data=row_data)
        self.editor_screen.ids.container.add_widget(self.dash_board)

    def update_dashboard(self, selected_sheet):
        """
        Update the dashboard whenever
        a new sheet is selected
        :param selected_sheet: Sheet selected by the user
        :return: None
        """
        self.current_sheet = selected_sheet
        sheet_data = self.render_data
        clean_data = self.clean_data(data=sheet_data[self.current_sheet])
        self.dash_board.max_cols = clean_data["max_cols"]
        self.reload_dashboard(data=clean_data["rows"])

    @staticmethod
    def clean_data(data):
        """
        Cleaning the data and make it in
        correct shape.
        :param data: Sheet data that needs to be clean.
        :return: dict
        """
        max_cols = data["max_cols"]
        data_setup = DataSetup(data=data, max_cols=max_cols)
        return data_setup.get_clean_data()

    def get_selected_data(self):
        """
        Collect the selected data
        :return: list
        """
        return self.dash_board.provide_selected_data()

    def reload_dashboard(self, data):
        """
        Reload the dashboard by deleting all
        its child widgets
        :param data: Data that use to render
        :return: None
        """
        self.dash_board.clear_widgets()  # Removing the old child widgets.
        self.dash_board.render_data(data=data)

    def save(self, is_overwrite=False):
        automate = Automate()
        automate.save_wb(
            file_path=self.render_data["file_path"],
            is_overwrite=is_overwrite,
            data=self.render_data
        )
        storage = Storage()
        if storage.is_first_store:
            storage.save(data=self.render_data)
        else:
            old_data = storage.read_all()
            filename = os.path.split(self.render_data["file_path"])[1]
            old_data[filename] = self.render_data
            storage.save(data=old_data)
