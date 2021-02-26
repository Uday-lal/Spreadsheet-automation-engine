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

    def __init__(self, text, size, bg_color=(1, 1, 1, 1), **kwargs):
        super(Cell, self).__init__(**kwargs)
        widget = MDGridLayout(cols=1)
        self.border_width = 1
        self.border_color = (0, 0, 0, 1)
        self.size = size
        self.is_car_component = False  # car(column and row) component which define the heading of column and rows.
        widget.size = self.size
        widget.pos = self.pos
        with widget.canvas:
            Color(self.border_color[0], self.border_color[1], self.border_color[2], self.border_color[3])
            Line(width=self.border_width, rectangle=(widget.x, widget.y, widget.width, widget.height))

        self.bg_color = bg_color

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
        Execute when user click to a particular cell
        :return: None
        """
        print(self.text)


class DashBoard:
    def __init__(self, wb_data, container):
        self.wb_data = wb_data
        self.container = container
        self.column_head_data = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def render_data(self, sheet):
        """
        Render the wb data in the form of datatable.
        :param sheet: Sheet to display.
        :return: None
        """
        _sheet = self.wb_data[sheet]
        rows = _sheet["rows"]
        column_head = " " + str(self.get_column_head(_sheet["max_col"]))
        column_head_list = []
        width, height = (100, 50)
        cell_container = MDGridLayout(cols=_sheet["max_col"])

        for head_data in column_head:
            column_head_list.append(head_data)

        rows.insert(0, column_head_list)

        for i in range(rows):
            row = rows.insert(0, i)
            for j in range(row):
                if j == 0 or i == 0:
                    cell = Cell(text=str(row[j]), size=(50, 25), bg_color=(191 / 255, 191 / 255, 191 / 255, 1))
                else:
                    cell = Cell(text=str(row[j]), size=(width, height))

                cell_container.add_widget(cell)

            self.container.add_widget(cell_container)

    def get_column_head(self, len_c):
        """
        Get the column head  such as
        if number of column is grater then 26
        then returns -> (AA, AB, AC, AD) and so on
        :param len_c: The of length of column.
        :return: str
        """
        return_value = self.column_head_data
        len_t = len(return_value)  # len_t: total length
        current_alpha_index = 0
        next_alpha_index = round(len_c - len_t) - 1

        for i in range(1, next_alpha_index + 1):
            current_alpha = str(return_value[current_alpha_index])
            next_alpha = str(return_value[i - 1])
            return_value = return_value + (current_alpha + next_alpha)

            if i % len_t == 0:
                current_alpha_index += 1

        return return_value
