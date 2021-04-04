"""
--------------------------------------------------------->
Copyrights (c) to UR's tech.ltd 2021. All rights reserved
Author: Uday lal
company: UR's tech.ltd
--------------------------------------------------------->

~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Defining all dynamic ui components
"""
from kivymd.uix.snackbar import Snackbar
from kivy.properties import (
    StringProperty,
    NumericProperty
)


class ErrorSnackBar(Snackbar):
    """Shows the command on the screen"""
    text = StringProperty(None)
    font_size = NumericProperty("15sp")
