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
from kivy.properties import ListProperty, NumericProperty, ObjectProperty, ColorProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.metrics import dp
from kivy.uix.scrollview import ScrollView
import string


class Cell(ButtonBehavior, Label):
    border_color = ColorProperty((0, 0, 0, 1))
    bg_color = ColorProperty((1, 1, 1, 1))

    def __init__(self, **kwargs):
        super(Cell, self).__init__(**kwargs)
        self.center = self.center
        self.padding_x = dp(4)

    def on_release(self):
        self.border_color = (0, 0, 1, 1)
        self.bg_color = (192 / 255, 206 / 255, 250 / 255, 1)
        print(self.text)


class BoardHeader(ScrollView):
    header = ObjectProperty(None)
    header_data = ListProperty([])
    max_cols = NumericProperty()

    def __init__(self, **kwargs):
        super(BoardHeader, self).__init__(**kwargs)
        self.render_headers()

    def render_headers(self):
        """
        Render the headers to the screen.
        :return: None
        """
        headers = Cell()

        for data in self.header_data:
            headers.text = str(data)
            headers.font_name = "assets/fonts/Heebo-Regular.ttf"
            headers.color = (0, 0, 0, 1)
            headers.bg_color = (199 / 255, 199 / 255, 199 / 255, 199 / 255, 1)
            self.add_widget(headers)


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
        """
        Render the workbook data to the screen.
        :return: None
        """
        recycle_view_dash_board = RecyclerDashBoardLayout(render_data=self.data, max_cols=self.max_cols)
        self.add_widget(recycle_view_dash_board)

    def get_headers(self):
        """
        Generate the header data based on the
        workbook data.
        :return: str
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
            return letters
