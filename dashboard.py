"""
--------------------------------------------------------->
Copyrights (c) to UR's tech.ltd 2021. All rights reserved
Author: Uday lal
company: UR's tech.ltd
--------------------------------------------------------->

~~~~~~~~~~~~~~~~~~~~~~~~~~
Making the dashboard.
"""
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line, Rectangle
from kivy.uix.label import Label


class Cell(Widget):
    """Making the cell"""

    def __init__(self, size, pos, text, **kwargs):
        super(Cell, self).__init__(**kwargs)
        if type(pos) is not tuple or type(
                size) is not tuple:  # Validating the required input values based on there type
            raise TypeError("type of pos and size should be tuple")

        self.size = size
        self.pos = pos
        self.text = str(text)
        self.label = Label(text=self.text, size=self.size, pos=self.pos)
        self.widget = Widget()
        self.border_width = 1
        self.border_color = (0, 0, 0, 1)
        with self.label.canvas:
            Color(self.border_color[0], self.border_color[1], self.border_color[2], self.border_color[3])
            Line(width=1, rectangle=(self.pos[0], self.pos[1] + 36, self.size[0], self.size[1]))
        self.widget.add_widget(self.label)

    def add_bg_color(self, color=(194 / 255, 190 / 255, 190 / 255, 1)):
        """
        Add the bg color to the cell
        :param color: Color to apply by default set to grey
        :return: None
        """
        with self.label.canvas.before:
            Color(color[0], color[1], color[2], color[3])
            Rectangle(size=self.size, pos=(self.pos[0], self.pos[1] + 36))
        self.widget.add_widget(self.label)

class DashBoard(Widget):
    pass
