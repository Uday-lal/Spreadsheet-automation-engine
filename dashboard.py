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
from screen import Base
from kivy.uix.anchorlayout import AnchorLayout


class Cell(Label):
    def __init__(self, **kwargs):
        super(Cell, self).__init__(**kwargs)
        self.center = self.center


class RecyclerDashBoardLayout(RecycleView):
    def __init__(self, render_data,  **kwargs):
        super(RecyclerDashBoardLayout, self).__init__(**kwargs)
        print(render_data)
        self.data = [{"text": str(data),"color": (0, 0, 0, 1), "font_name": "assets/fonts/Heebo-Regular.ttf"}
                     for data in render_data]


class DashBoard(AnchorLayout):
    def __init__(self, **kwargs):
        super(DashBoard, self).__init__(**kwargs)

    def render_data(self, data):
        recycle_view_dash_board = RecyclerDashBoardLayout(render_data=data)
        self.add_widget(recycle_view_dash_board)
