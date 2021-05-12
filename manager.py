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

from screens.home_screen import HomeScreen
from screens.editor_screen import EditorScreen
from dashboard import DashBoard
from mof_library.dataSetup_mof import DataSetup
from kivy.properties import StringProperty, ListProperty
from Automate import Automate
from storage import Storage
from datetime import datetime
import webbrowser
import os


class Manager(ScreenManager):
    current_sheet = StringProperty()
    master_selected_data = ListProperty()
    str_index_data = ListProperty()

    def __init__(self, **kwargs):
        super(Manager, self).__init__(**kwargs)
        self.home_screen = HomeScreen(name="home_screen")
        self.editor_screen = EditorScreen(name="editor_screen")
        self.add_widget(self.home_screen)
        self.add_widget(self.editor_screen)
        self.render_home_screen_content()

    def screen_transition_home(self):
        """
        Define screen transition home
        :return: None
        """
        if self.current_screen.name != "home_screen":
            self.transition.direction = "down"
            self.current = "home_screen"

    @staticmethod
    def open_web_browser():
        """
        Define screen transition tutorial
        :return: None
        """
        webbrowser.open("https://chrunch-tech.github.io/Propoint-website/")

    def render_empty_home_screen(self):
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
        data_setup = DataSetup(data=data)
        clean_data = data_setup.get_clean_data()
        return clean_data

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

    def save(self, updated_path=None):
        """
        Saving the workbook data to the
        as the history
        :param updated_path: path on which user want
         to save there workbook if they select don't overwrite
        :return: None
        """
        self.current_date = datetime.today().strftime("%d-%m-%Y")
        automate = Automate()
        automate.save_wb(
            file_path=self.render_data["file_path"],
            data=self.render_data,
            updated_path=updated_path
        )
        storage = Storage()
        if storage.is_first_store:
            path, filename = os.path.split(self.render_data["file_path"])
            root = {filename: self.render_data}
            root[filename]["date_of_modify"] = self.current_date
            storage.save(data=root)
        else:
            old_data = storage.read_all()
            filename = os.path.split(self.render_data["file_path"])[1]
            old_data[filename] = self.render_data
            old_data[filename]["date_of_modify"] = self.current_date
            storage.save(data=old_data)

    def render_home_screen_content(self):
        """
        Surface users history
        :return: None
        """
        save_path = os.path.join(os.path.expanduser("~"), "AppData\\Roaming")
        if "Propoint" not in os.listdir(save_path):
            self.render_empty_home_screen()
        else:
            self.storage = Storage()
            try:
                all_data = self.storage.read_all()
            except FileNotFoundError:
                all_data = {}

            if all_data == {}:
                self.render_empty_home_screen()
            else:
                history_data = self.storage.read_all()
                self.home_screen.present_users_history(history_data=history_data)

    def view_button_callback(self, instance):
        """
        View the wb from history_data
        :param instance: history_car instance
        :return: None
        """
        self.editor_screen.ids.container.clear_widgets()
        filename = instance.title
        file_data = self.storage.read(filename=filename)
        self.render_wb_data(render_data=file_data)
        self.transition.direction = "left"
        self.current = "editor_screen"

    def delete(self, instance):
        """
        Delete wb history_data
        :param instance: history_card instance
        :return: None
        """
        filename = instance.title
        self.storage.delete_history(filename=filename)
        self.clear_home_screen()
        self.render_home_screen_content()

    def clear_dashboard(self):
        """
        Clear the dashboard
        :return: None
        """
        self.dash_board.clear_widgets()

    def clear_home_screen(self):
        """
        Clearing home screen
        to render updated data
        :return: None
        """
        self.home_screen.ids.main_box_layout.remove_widget(widget=self.home_screen.ids.history_card_scroll_view)
