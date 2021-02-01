"""
--------------------------------------------------------->
Copyrights (c) to UR's tech.ltd. All rights reserved
Author: Uday lal
company: UR's tech.ltd
--------------------------------------------------------->
"""

from kivy.uix.screenmanager import Screen


class Base(Screen):
    def rail_open(self):
        if self.ids.rail.rail_state == "open":
            self.ids.rail.rail_state = "close"
        else:
            self.ids.rail.rail_state = "open"


class HomeScreen(Base):
    pass


class SettingScreen(Base):
    pass


class TutorialScreen(Base):
    pass


class EditorScreen(Screen):
    pass
