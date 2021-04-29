"""
--------------------------------------------------------->
Copyrights (c) to UR's tech.ltd 2021. All rights reserved
Author: Uday lal
company: UR's tech.ltd
--------------------------------------------------------->

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Defining the error snack bars which going to present
to the user if something went wrong during runtime
"""
from components import MsgSnackBar
from kivy.core.window import Window


def something_went_wrong():
    """
    Show error to the user if
    any error happen during runtime
    :return: None
    """
    snack_bar = MsgSnackBar(
        text="Oops :(, something went wrong please try again!",
        snackbar_x="10dp",
        snackbar_y="10dp"
    )
    snack_bar.size_hint_x = (Window.width - (snack_bar.snackbar_x * 2)) / Window.width
    snack_bar.open()


def rows_selection_error():
    """
    Show error to the user if
    row master cell is selected
    :return: None
    """
    snack_bar = MsgSnackBar(
        text="Sorry! This version of Propoint dose not support any operation on rows",
        snackbar_x="10dp",
        snackbar_y="10dp"
    )
    snack_bar.size_hint_x = (Window.width - (snack_bar.snackbar_x * 2)) / Window.width
    snack_bar.open()
