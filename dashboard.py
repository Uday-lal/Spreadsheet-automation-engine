"""
--------------------------------------------------------->
Copyrights (c) to UR's tech.ltd 2021. All rights reserved
Author: Uday lal
company: UR's tech.ltd
--------------------------------------------------------->

~~~~~~~~~~~~~~~~~~~~~~~~~~
Making the dashboard.
"""
from kivy.uix.label import Label
from kivy.graphics import Color, Line, Rectangle
from kivy.uix.widget import Widget
from kivy.uix.behaviors import ButtonBehavior


class Cell(Widget, ButtonBehavior):
    """Building the cell widget."""

    def __init__(self, size, pos, is_car_section=False, **kwargs):
        super(Cell, self).__init__(**kwargs)
        self.border_width = 1
        self.border_color = (0, 0, 0, 1)
        self.text = ""
        label = Label()
        self.pos_x, self.pos_y = pos
        self.width, self.height = size

        with self.canvas:
            Color(self.border_color[0], self.border_color[1], self.border_color[2], self.border_color[3])
            Line(width=self.border_width, rectangle=(self.pos_x, self.pos_y, self.width, self.height))

        if is_car_section:  # car(column and row) section validation
            self.add_bg_color()

        label.text = str(self.text)
        label.font_name = "assets/fonts/Heebo-Regular.ttf"
        label.color = (0, 0, 0, 1)
        label.center = self.center
        self.add_widget(label)

    def add_bg_color(self, color=(194 / 255, 194 / 255, 194 / 255, 1)):
        """
        Add the bg color to the cell
        :param color: Color to apply by default set to grey
        :return: None
        """
        with self.canvas.before:
            Color(color[0], color[1], color[2], color[3])
            Rectangle(pos=(self.pos_x, self.pos_y), size=(self.width, self.height))

    def on_release(self, on_release_func=None):
        """
        Execute when this widget in click
        :param on_release_func: Function that execute when this widget in click
        :return: type(on_release_func)
        """
        return on_release_func


class DashBoard(Widget):
    pass
