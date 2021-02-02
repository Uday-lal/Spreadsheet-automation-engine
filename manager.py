"""
--------------------------------------------------------->
Copyrights (c) to UR's tech.ltd 2021. All rights reserved
Author: Uday lal
company: UR's tech.ltd
--------------------------------------------------------->
"""
from kivy.uix.screenmanager import ScreenManager
from screen import *
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.label import MDLabel


class Manger(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.home_screen = HomeScreen(name="home_screen")
        self.setting_screen = SettingScreen(name="setting_screen")
        self.tutorial_screen = TutorialScreen(name="tutorial_screen")
        self.editor_screen = EditorScreen(name="editor_screen")
        self.add_widget(self.home_screen)
        self.add_widget(self.setting_screen)
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

    def screen_transition_setting(self):
        """
        Define screen transition setting
        :return: None
        """
        if self.current_screen != "setting_screen":
            if self.current_screen.name == "home_screen":
                self.transition.direction = "up"
                self.current = "setting_screen"
            else:
                self.transition.direction = "down"
                self.current = "setting_screen"

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
        grid_layout = GridLayout()
        box_layout = BoxLayout()
        label = MDLabel()
        labels = []
        sheets = render_data["sheets"]

        for sheet in sheets:
            render_data_copy = render_data.copy()
            del render_data_copy[sheet]["max_col"]
            del render_data_copy[sheet]["max_row"]
            current_sheet = render_data_copy[sheet]
            for col in current_sheet:
                current_col = current_sheet[col]
                for data in current_col:
                    label.text = str(data)
                    label.font_name = "assets/fonts/Heebo-Regular.ttf"
                    labels.append(label)

        box_layout.add_widget(labels[0])

        grid_layout.add_widget(box_layout)
        self.editor_screen.add_widget(grid_layout)
