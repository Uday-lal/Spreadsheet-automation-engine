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
    BooleanProperty,
    ObjectProperty
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
    column_index = NumericProperty()
    row_index = NumericProperty()

    def __init__(self, **kwargs):
        super(Cell, self).__init__(**kwargs)
        self.center = self.center
        self.font_name = "assets/fonts/Heebo-Regular.ttf"
        self.padding_x = dp(4)

    def on_release(self):
        """
        Defining the logic if any cell click.
        :return: None
        """
        self.is_selected = True
        dash_board_helper = DashBoardHelper()
        dash_board_helper.cell = self
        dash_board_helper.on_click()


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
                "is_master": data[1],
                "is_selected": data[2],
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


class DashBoardHelper(DashBoard):
    cell = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(DashBoardHelper, self).__init__(**kwargs)

    def on_click(self):
        """
        Define the response when any cell is clicked
        :return: None
        """
        if self.cell.is_master:
            print(self.data)
            self.master_selection(column_index=self.cell.column_index)
        # if cell.is_selected:
        #     self.selection()

    def master_selection(self, column_index):
        """
        Update the data dict on the master selection
        :param column_index: Column index of the cell
        :return: None
        """
        while True:
            try:
                fia_data = self.fast_iter_algorithm()  # Data comes from fia => (fast_iter_algorithm)
                cell_data = next(fia_data)[column_index]
                cell_data[2] = True
            except StopIteration:
                break

    def selection(self):
        pass

    def fast_iter_algorithm(self):
        data_len = len(self.data)
        for i in range(data_len):
            if i == (data_len + 1):
                raise StopIteration()
            data = self.data[i] if i % 2 == 0 else self.data[data_len - i]
            yield data
