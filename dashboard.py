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
import string


class Cell(ButtonBehavior, Label):
    border_color = ColorProperty((0, 0, 0, 1))
    bg_color = ColorProperty((1, 1, 1, 1))
    selected_border_color = ColorProperty((0, 0, 1, 1))
    selected_color = ColorProperty((192 / 255, 206 / 255, 250 / 255, 1))
    is_selected = BooleanProperty(False)

    def __init__(self, **kwargs):
        super(Cell, self).__init__(**kwargs)
        self.center = self.center
        self.font_name = "assets/fonts/Heebo-Regular.ttf"
        self.padding_x = dp(4)

    def on_release(self):
        self.is_selected = True
        print(self.text)


class RecyclerDashBoardLayout(RecycleView):
    max_cols = NumericProperty()
    cols_minimum = DictProperty()

    def __init__(self, render_data, max_cols, **kwargs):
        super(RecyclerDashBoardLayout, self).__init__(**kwargs)
        self.max_cols = max_cols
        self.get_cols_minimum()
        self.data = [
            {
                "text": str(data),
                "size": (100, 25)
            }
            for row_data in render_data for data in row_data
        ]

    def get_cols_minimum(self):
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
        headers = self.get_headers()
        headers.insert(0, "")
        data = self.insert_row_master()
        data.insert(0, headers)
        self.max_cols = len(data[0])
        recycle_view_dash_board = RecyclerDashBoardLayout(render_data=data, max_cols=self.max_cols)
        self.add_widget(recycle_view_dash_board)

    def get_headers(self):
        """
        Generate the header data based on the
        workbook data.
        :return: list
        """
        letters = [letter for letter in string.ascii_uppercase]

        if len(letters) < self.max_cols:
            max_len = len(letters)
            first_letter_i = round(self.max_cols / max_len)
            last_letter_i = self.max_cols - max_len

            for fli in range(first_letter_i):
                first_letter = letters[fli]
                for lli in range(last_letter_i):
                    last_letter = letters[lli]
                    letter = first_letter + last_letter
                    letters.append(letter)

            return letters[0:self.max_cols]

        else:
            return letters[0:self.max_cols]

    def insert_row_master(self):
        index = 0
        for row_data in self.data:
            index += 1
            row_data.insert(0, index)

        return self.data
