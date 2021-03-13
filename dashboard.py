"""
--------------------------------------------------------->
Copyrights (c) to UR's tech.ltd 2021. All rights reserved
Author: Uday lal
company: UR's tech.ltd
--------------------------------------------------------->

Special thanks to the information at:
https://stackoverflow.com/questions/50219281/python-how-to-add-vertical-scroll-in-recycleview

~~~~~~~~~~~~~~~~~~~~~~~~~~
Making the dashboard.
"""
from kivy.uix.recycleview import RecycleView
from kivy.uix.label import Label
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import (
    ListProperty,
    NumericProperty,
    ColorProperty,
    DictProperty,
    BooleanProperty
)
from kivy.uix.behaviors import ButtonBehavior
from kivy.metrics import dp


class Cell(ButtonBehavior, Label):
    border_color = ColorProperty((0, 0, 0, 1))
    bg_color = ColorProperty((1, 1, 1, 1))
    selected_border_color = ColorProperty((0, 0, 1, 1))
    selected_color = ColorProperty((192 / 255, 206 / 255, 250 / 255, 1))
    master_bg_color = ColorProperty((191 / 255, 191 / 255, 191 / 255, 1))
    is_selected = BooleanProperty(False)
    is_master = BooleanProperty(False)

    def __init__(self, **kwargs):
        super(Cell, self).__init__(**kwargs)
        self.center = self.center
        self.font_name = "assets/fonts/Heebo-Regular.ttf"
        self.padding_x = dp(4)


class RecyclerDashBoardLayout(RecycleView):
    max_cols = NumericProperty()
    cols_minimum = DictProperty()

    def __init__(self, render_data, max_cols, **kwargs):
        super(RecyclerDashBoardLayout, self).__init__(**kwargs)
        self.max_cols = max_cols
        print(f"Recycler view {str(self.max_cols)}")
        self.get_cols_minimum()
        self.data = [
            {
                "text": str(data[0]),
                "size": (100, 25),
                "is_master": data[1],
                "is_selected": data[2]
            }
            for row_data in render_data for data in row_data
        ]

    def get_cols_minimum(self):
        """
        Making the width of each column in the dashboard
        :return: None
        """
        for i in range(self.max_cols):
            self.cols_minimum[i] = 200


class DashBoard(MDBoxLayout):
    data = ListProperty([])
    max_cols = NumericProperty()

    def __init__(self, **kwargs):
        super(DashBoard, self).__init__(**kwargs)
        self.orientation = "vertical"

    def render_data(self):
        """
        Render the workbook data to the screen.
        :return: None
        """
        recycle_view_dash_board = RecyclerDashBoardLayout(render_data=self.data, max_cols=self.max_cols)
        self.add_widget(recycle_view_dash_board)
