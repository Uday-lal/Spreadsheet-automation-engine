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
from automate import splitting_algorithm
from kivymd.uix.behaviors import HoverBehavior
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.theming import ThemableBehavior
from kivymd.uix.label import MDLabel
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView


class HoverItem(MDGridLayout, ThemableBehavior, HoverBehavior):
    """Custom item implementing hover behavior."""

    @staticmethod
    def on_enter(*args):
        """
        Run when the cursor enters
        :param args: *args
        :return: None
        """
        print("hover")

    @staticmethod
    def on_leave(*args):
        """
        Run when the cursor leaves
        :param args: *args
        :return: None
        """
        print("Not hover")


class Manager(ScreenManager):
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
        sheet = render_data[render_data["sheets"][0]]
        rows = sheet["rows"]
        bg_color = (251 / 255, 237 / 255, 255 / 255, 1)
        heading_introPart = splitting_algorithm(wb_data=render_data)
        heading = heading_introPart["heading"]
        intro_part = heading_introPart["intro_part"]
        width, height = 100, 50
        pos_x = self.editor_screen.ids.rail.width
        pos_y = Window.height / 2
        main_grid_container = MDGridLayout()
        scroll_view = ScrollView(scroll_type=['bars'],
                                 bar_width='9dp',
                                 scroll_wheel_distance=100)

        data_table_container = self.editor_screen.ids.data_table_container

        for row in rows:
            for data in row:
                grid_layout = MDGridLayout(cols=1)
                label = MDLabel()
                label.text = str(data)
                grid_layout.md_bg_color = bg_color
                grid_layout.size_hint = (None, None)
                grid_layout.size = (width, height)
                grid_layout.pos = (pos_x, pos_y)

                if row == heading:
                    label.font_name = "assets/fonts/Heebo-Bold.ttf"
                else:
                    label.font_name = "assets/fonts/Heebo-Regular.ttf"

                if intro_part is not None:
                    for intro_data in intro_part:
                        if intro_data == rows:
                            label.font_name = "assets/fonts/Heebo-ExtraBold.ttf"
                            grid_layout.cols = 1

                grid_layout.spacing = 2
                grid_layout.add_widget(label)
                main_grid_container.add_widget(grid_layout)
                pos_x += width

            pos_y -= height
            pos_x = self.editor_screen.ids.rail.width

        main_grid_container.cols = sheet["max_col"]
        main_grid_container.md_bg_color = bg_color
        main_grid_container.size_hint = (None, None)
        main_grid_container.bind(minimum_height=main_grid_container.setter('height'),
                                 minimum_width=main_grid_container.setter('width'))
        scroll_view.add_widget(main_grid_container)
        data_table_container.md_bg_color = bg_color
        data_table_container.size = (Window.width, Window.height)
        data_table_container.add_widget(scroll_view)
