"""
--------------------------------------------------------->
Copyrights (c) to UR's tech.ltd. All rights reserved
Author: Uday lal
company: UR's tech.ltd
--------------------------------------------------------->
"""
from kivy.uix.screenmanager import ScreenManager
from screen import *


class Manger(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(HomeScreen(name="home_screen"))
        self.add_widget(SettingScreen(name="setting_screen"))
        self.add_widget(TutorialScreen(name="tutorial_screen"))
        self.add_widget(EditorScreen(name="editor_screen"))

    def screen_transition_home(self):
        if self.current_screen.name != "home_screen":
            self.transition.direction = "down"
            self.current = "home_screen"

    def screen_transition_setting(self):
        if self.current_screen != "setting_screen":
            if self.current_screen.name == "home_screen":
                self.transition.direction = "up"
                self.current = "setting_screen"
            else:
                self.transition.direction = "down"
                self.current = "setting_screen"

    def screen_transition_tutorial(self):
        if self.current_screen.name != "editor_screen":
            self.transition.direction = "up"
            self.current = "tutorial_screen"
