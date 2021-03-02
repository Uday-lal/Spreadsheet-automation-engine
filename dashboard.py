"""
--------------------------------------------------------->
Copyrights (c) to UR's tech.ltd 2021. All rights reserved
Author: Uday lal
company: UR's tech.ltd
--------------------------------------------------------->
~~~~~~~~~~~~~~~~~~~~~~~~~~
Making the dashboard.
"""
from kivy.uix.recycleview import RecycleView
from kivy.uix.label import Label
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import ListProperty, NumericProperty
from kivy.uix.behaviors import ButtonBehavior


class Cell(ButtonBehavior, Label):
    def __init__(self, **kwargs):
        super(Cell, self).__init__(**kwargs)
        self.center = self.center

    def on_release(self):
        print(self.text)


class RecyclerDashBoardLayout(RecycleView):
    max_cols = NumericProperty()

    def __init__(self, render_data, max_cols, **kwargs):
        super(RecyclerDashBoardLayout, self).__init__(**kwargs)
        self.max_cols = max_cols
        self.data = [
            {
                "text": str(data),
                "font_name": "assets/fonts/Heebo-Regular.ttf",
                "color": (0, 0, 0, 1)
            }
            for row_data in render_data for data in row_data
        ]


class DashBoard(MDBoxLayout):
    data = ListProperty([])
    max_cols = NumericProperty()

    def __init__(self, **kwargs):
        super(DashBoard, self).__init__(**kwargs)
        self.orientation = "vertical"

    def render_data(self):
        recycle_view_dash_board = RecyclerDashBoardLayout(render_data=self.data, max_cols=self.max_cols)
        self.add_widget(recycle_view_dash_board)
