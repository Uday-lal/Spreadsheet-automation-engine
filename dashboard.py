"""
--------------------------------------------------------->
Copyrights (c) to UR's tech.ltd 2021. All rights reserved
Author: Uday lal
company: UR's tech.ltd
--------------------------------------------------------->

~~~~~~~~~~~~~~~~~~~~~~~~~~
Making the dashboard.
"""
from kivymd.uix.gridlayout import MDGridLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.graphics import Line, Color
from kivy.uix.behaviors import ButtonBehavior


class Cell(ButtonBehavior, Widget):
    """Make the cell and define all its functionality"""

    def __init__(self, pos, text, size, **kwargs):
        super(Cell, self).__init__(**kwargs)
        widget = MDGridLayout(cols=1)
        self.border_width = 1
        self.border_color = (0, 0, 0, 1)
        self.pos = pos
        self.size = size
        self.is_car_component = False  # car(column and row) component 
        widget.size = self.size
        widget.pos = self.pos
        with widget.canvas:
            Color(self.border_color[0], self.border_color[1], self.border_color[2], self.border_color[3])
            Line(width=self.border_width, rectangle=(widget.x, widget.y, widget.width, widget.height))

        self.bg_color = (1, 1, 1, 1)

        widget.md_bg_color = self.bg_color
        label = Label()
        self.text = str(text)
        label.text = self.text
        label.font_name = "assets/fonts/Heebo-Regular.ttf"
        label.color = (0, 0, 0, 1)
        label.center = widget.center
        widget.add_widget(label)
        self.add_widget(widget)

    def on_release(self):
        """
        Execute when user click to a perticular cell
        :return: None
        """
        pass


class DashBoard:
    def __init__(self, render_data, container):
        self.render_data = render_data
        self.container = container

    def render_data(self):
        pass
