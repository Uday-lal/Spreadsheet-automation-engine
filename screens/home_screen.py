"""
--------------------------------------------------------->
Copyrights (c) to UR's tech.ltd 2021. All rights reserved
Author: Uday lal
company: UR's tech.ltd
--------------------------------------------------------->

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Defining the home screen
"""

from . import Base
from kivy.properties import NumericProperty
from kivy.uix.scrollview import ScrollView
from kivy.utils import get_color_from_hex
from components import HistoryCard, HistoryCardContainer
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.dialog import MDDialog


class HomeScreen(Base):
    number_of_widget = NumericProperty()

    def present_users_history(self, history_data):
        key_list = history_data.keys()
        scroll_view = ScrollView(
            scroll_type=['bars'],
            bar_width='9dp',
            scroll_wheel_distance=100
        )
        history_card_container = HistoryCardContainer()
        history_card_container.rail_width = self.ids.rail.width
        history_card_container.clear_widgets()
        self.ids["history_card_scroll_view"] = scroll_view
        for key in key_list:
            self.history_card = HistoryCard()
            self.history_card.title = key
            self.history_card.date_of_modify = history_data[key]["date_of_modify"]
            history_card_container.card_width = self.history_card.width
            history_card_container.add_widget(self.history_card)

        history_card_container.spacing = 30
        history_card_container.padding = 15
        history_card_container.bind(minimum_height=history_card_container.setter("height"))
        history_card_container.rail_width = self.ids.rail.width
        scroll_view.add_widget(history_card_container)
        self.ids.main_box_layout.add_widget(scroll_view)

    def open_dialog(self, card_instance):
        self.clicked_card = card_instance
        self.dialog = MDDialog(
            text=f"Do you want to view {card_instance.title} or delete {card_instance.title}?",
            buttons=[
                MDRectangleFlatButton(
                    text="View",
                    text_color=get_color_from_hex("#0074d4"),
                    line_color=get_color_from_hex("#219bff")
                ),
                MDRectangleFlatButton(
                    text="Delete",
                    text_color=(1, 0, 0, 1),
                    line_color=(1, 0, 0, 1)
                )
            ]
        )
        self.dialog.buttons[0].bind(on_release=lambda instance: self.dialog_callback(instance=instance))
        self.dialog.buttons[1].bind(on_release=lambda instance: self.dialog_callback(instance=instance))
        self.dialog.open()

    def dialog_callback(self, instance):
        if instance.text == "View":
            self.manager.view_button_callback(instance=self.clicked_card)
        else:
            self.manager.delete(instance=self.clicked_card)
        self.dialog.dismiss()
