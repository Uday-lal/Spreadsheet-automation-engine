"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Defining validation for selection mode
"""
from Automate.coc_engine.clean_command import CleanCommand


class SelectionModeValidation:
    def __init__(self, command, headers):
        try:
            self.command = CleanCommand(commands=command).shape_input() if command != "new" else command
        except IndexError:
            self.command = ""
        self.headers = self.clean_headers(headers)

    def validate(self):
        """
        Vaidating the entered command
        :return: bool
        """
        if self.command == "new":
            return True
        else:
            try:
                command = self.command[0]
            except IndexError:
                command = ""
            if command in self.headers and len(self.command) == 1:
                return True
        return False

    @staticmethod
    def clean_headers(headers):
        """
        Remove the is_master and is_selected boolean
        from the header
        :param headers: list
        :return: list
        """
        clean_headers = []
        for header in headers:
            header_value = header[0]
            if header_value != "":
                clean_headers.append(header_value)

        return clean_headers
