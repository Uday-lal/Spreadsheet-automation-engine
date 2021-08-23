"""
~~~~~~~~~~~~~~~~~~~~~~~
COC(Coordinate Operation Controller) is type engine which is
responsible for handle all the inputs coming from input box
to select cells to perform mathematical logic
"""
import re
from .clean_command import CleanCommand


class CoordinateOperationController:
    def __init__(self, headers, commands):
        self.commands = str(commands)
        self.headers = headers
        self.clean_command = CleanCommand(commands=self.commands)
        self.operators = {  # Defining the possible operators with several commands
            "+": "add",
            "-": "sub",
            "/": "divide",
            "*": "multiply",
            "=": "equal_to"
        }

    def provide_data_for_execution(self):
        """
        Execute the command that are
        given.
        :return: dict
        """
        self.data_for_execution = {}
        shape_input = self.clean_command.shape_input()
        self.root_key = "new"
        operator_coming_times = 0
        if "=" in shape_input:
            self.root_key = self.data_index(command=[shape_input[0]])[0]
            shape_input = shape_input[2:len(shape_input)]
        self.data_for_execution[self.root_key] = []

        for i, command in enumerate(shape_input):
            operator = self.operators[command] if command in self.operators else None

            if operator is not None:
                operator_coming_times += 1
                node = {}
                if operator_coming_times == 1:
                    last_value, next_value = self.data_index([shape_input[i - 1]])[0], self.data_index(
                        [shape_input[i + 1]])[0]
                    node[operator] = [last_value, next_value]
                    self.data_for_execution[self.root_key].append(node)
                else:
                    next_value = self.data_index(command=[shape_input[i + 1]])[0] if not shape_input[
                        i + 1].isdigit() else \
                        ("isdigit", int(shape_input[i + 1]))
                    node[operator] = [next_value]
                    self.data_for_execution[self.root_key].append(node)

        self.arrange()
        return self.data_for_execution

    def data_index(self, command):
        """
        Returns the index of each command
        or input presented in the headers

        --------------------------------
        sample input: ["B", "*", "C"]
        --------------------------------
        :param command: Input data base on which it going to return some value
        :return: list
        """
        headers = self.headers

        return_data = []

        for value in command:
            if value.isdigit() or "." in value:
                _value = int(value) if "." not in value else float(value)
                return_data.append(("isdigit", _value))
                break
            for header in headers:
                if len(value) == 1:
                    if value in header:
                        return_data.append(headers.index(header))
                        break
                else:
                    row_index, column_index = re.match(r"([a-z]+)([0-9]+)", value, re.I).groups()
                    if row_index in header:
                        return_data.append((headers.index(header), int(column_index)))
                        break

        return return_data

    def arrange(self):
        data_for_execution = self.data_for_execution[self.root_key]
        i = 0
        while True:
            i += 1
            try:
                node = data_for_execution[i]
            except IndexError:
                break
            operator = list(node.keys())[0]
            node_value = node[operator]

            if operator == "multiply" or operator == "divide":
                last_node = data_for_execution[i - 1]
                last_node_operator = list(last_node.keys())[0]
                if last_node_operator != "multiply" and last_node_operator != "divide":
                    last_node_value = last_node[last_node_operator]
                    last_node_value = last_node_value[1] if len(last_node_value) == 2 else last_node_value[0]
                    data_for_execution[i] = {operator: [last_node_value, node_value[0]]}
                    data_for_execution.insert(i, {last_node_operator: last_node_value, "is_universal": True})
                    i += 1
