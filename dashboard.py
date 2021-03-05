"""
--------------------------------------------------------->
Copyrights (c) to UR's tech.ltd 2021. All rights reserved
Author: Uday lal
company: UR's tech.ltd
--------------------------------------------------------->

Special thanks for the info at:
`https://stackoverflow.com/questions/50219281/python-how-to-add-vertical-scroll-in-recycleview`

~~~~~~~~~~~~~~~~~~~~~~~~~~
Making the dashboard.
"""
from kivy.uix.recycleview import RecycleView
from kivy.uix.label import Label
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import ListProperty, NumericProperty, ObjectProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.metrics import dp
from kivy.uix.scrollview import ScrollView


class Cell(ButtonBehavior, Label):
    bg_color = ListProperty([1, 1, 1, 1])

    def __init__(self, **kwargs):
        super(Cell, self).__init__(**kwargs)
        self.center = self.center
        self.padding_x = dp(4)

    def on_release(self):
        print(self.text)


class BoardHeader(ScrollView):
    header_data_obj = ObjectProperty()
    header_data = ListProperty([])

    def __init__(self, **kwargs):
        super(BoardHeader, self).__init__(**kwargs)
        self.header_data_obj = Cell()

        for data in self.header_data:
            self.header_data_obj.text = str(data)
            self.header_data_obj.font_name = "assets/fonts/Heebo-Regular.ttf"
            self.header_data_obj.color = (0, 0, 0, 1)


class RecyclerDashBoardLayout(RecycleView):
    max_cols = NumericProperty()

    def __init__(self, render_data, max_cols, **kwargs):
        super(RecyclerDashBoardLayout, self).__init__(**kwargs)
        self.max_cols = max_cols
        self.scroll_type = ["bars"]
        self.bar_width = dp(9)
        self.scroll_wheel_distance = 100
        self.data = [
            {
                "text": str(data),
                "font_name": "assets/fonts/Heebo-Regular.ttf",
                "color": (0, 0, 0, 1),
                "size": (100, 25)
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
