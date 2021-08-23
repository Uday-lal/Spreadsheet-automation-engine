"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Defining all dynamic ui components
"""
from kivymd.uix.snackbar import Snackbar
from kivy.properties import (
    StringProperty,
    NumericProperty,
    ColorProperty
)
from kivymd.uix.list import OneLineAvatarIconListItem
from kivymd.uix.button import MDRectangleFlatIconButton
from kivymd.uix.card import MDCard
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout


class MsgSnackBar(Snackbar):
    """Shows the command on the screen"""
    text = StringProperty(None)
    font_size = NumericProperty("15sp")


class Item(OneLineAvatarIconListItem):
    text = StringProperty()


class CancelButton(MDRectangleFlatIconButton):
    icon = "cancel"
    text = "Cancel"
    text_color = ColorProperty((1, 0, 0, 1))
    line_color = ColorProperty((1, 0, 0, 1))
    icon_color = ColorProperty((0, 0, 0, 1))


class HistoryCard(MDCard):
    title = StringProperty()
    date_of_modify = StringProperty()


class HistoryCardContainer(GridLayout):
    rail_width = NumericProperty()


class NotOverwriteDialogContent(BoxLayout):
    pass
