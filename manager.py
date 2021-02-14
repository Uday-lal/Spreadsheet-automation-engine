"""
--------------------------------------------------------->
Copyrights (c) to UR's tech.ltd 2021. All rights reserved
Author: Uday lal
company: UR's tech.ltd
--------------------------------------------------------->
"""
from kivy.uix.screenmanager import ScreenManager
from screen import HomeScreen, SettingScreen, TutorialScreen, EditorScreen
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.image import Image


class Manager(ScreenManager):
    def __init__(self, **kwargs):
        super(Manager, self).__init__(**kwargs)
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
