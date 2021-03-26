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
    NumericProperty,
    ColorProperty,
    DictProperty,
    BooleanProperty,
    ListProperty,
    ObjectProperty
)
from kivy.uix.behaviors import ButtonBehavior
from kivy.metrics import dp
from kivy.uix.popup import Popup
from kivymd.uix.gridlayout import MDGridLayout

processing_data = []


class PopupContent(MDGridLayout):
    clicked_cell = ObjectProperty()
    _popup = ObjectProperty()


class Cell(ButtonBehavior, Label):
    border_color = ColorProperty((0, 0, 0, 1))
    bg_color = ColorProperty((1, 1, 1, 1))
    selected_border_color = ColorProperty((0, 0, 1, 1))
    selected_color = ColorProperty((192 / 255, 206 / 255, 250 / 255, 1))
    master_bg_color = ColorProperty((191 / 255, 191 / 255, 191 / 255, 1))
    is_selected = BooleanProperty(False)
    is_master = BooleanProperty(False)
    column_index = NumericProperty()
    row_index = NumericProperty()

    def __init__(self, **kwargs):
        super(Cell, self).__init__(**kwargs)
        self.center = self.center
        self.font_name = "assets/fonts/Heebo-Regular.ttf"
        self.padding_x = dp(4)
        if self.is_selected:
            self.give_selected_styles()

    def on_release(self):
        """
        Respond to the click event
        :return: None
        """
        if not self.is_master:
            popup = Popup(
                title="Update cell",
                content=PopupContent(),
                size_hint=(None, None),
                size=(400, 200),
                separator_height=1
            )
            popup.content.clicked_cell = self
            popup.content._popup = popup
            popup.open()

    def give_selected_styles(self):
        """
        Defining the selected styles
        so that it could change based
        on the state of is_selected
        :return: None
        """
        self.bg_color = (148 / 255, 189 / 255, 255 / 255, 1)
        self.border_color = (0, 0, 1, 1)


class RecyclerDashBoardLayout(RecycleView):
    max_cols = NumericProperty()
    cols_minimum = DictProperty()

    def __init__(self, render_data, max_cols, **kwargs):
        super(RecyclerDashBoardLayout, self).__init__(**kwargs)
        self.max_cols = max_cols
        self.get_cols_minimum()
        self.data = [
            {
                "text": str(data[0]),
                "size": (100, 25),
                "is_selected": data[2],
                "is_master": data[1],
                "column_index": ci,
                "row_index": ri
            }
            for ri, row_data in enumerate(render_data) for ci, data in enumerate(row_data)
        ]

    def get_cols_minimum(self):
        """
        Making the width of each column in the dashboard
        :return: None
        """
        for i in range(self.max_cols):
            self.cols_minimum[i] = 200


class DashBoard(MDBoxLayout):
    max_cols = NumericProperty()
    data = ListProperty()

    def __init__(self, **kwargs):
        super(DashBoard, self).__init__(**kwargs)
        self.orientation = "vertical"

    def render_data(self, data):
        """
        Render the workbook data to the screen.
        :return: None
        """
        self.data = data
        recycle_view_dash_board = RecyclerDashBoardLayout(render_data=self.data, max_cols=self.max_cols)
        self.add_widget(recycle_view_dash_board)
