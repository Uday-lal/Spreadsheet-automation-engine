"""
--------------------------------------------------------->
Copyrights (c) to UR's tech.ltd 2021. All rights reserved
Author: Uday lal
company: UR's tech.ltd
--------------------------------------------------------->

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Store going hold each instance of the
program.
for example: value of the variables etc
"""


class Store:
    def __init__(self):
        self.store_state = []
        self.var_list = []

    def save(self, data_to_safe):
        """
        Save the given data into
        the store
        :param data_to_safe: Pair to variable and its value that needs to be save
        :return: None
        """
        var, value = data_to_safe
        if (var, value) in self.store_state:
            store_index = self.store_state.index((var, value))
            self.store_state[store_index] = (var, value)
        else:
            self.store_state.append((var, value))
        
        self.var_list.append(var)

    def read(self, key):
        """
        Read selected data state form
        the store
        :param key: the variable key which assign to a value
        :return: any
        """
        index = self.var_list.index(key)
        return self.store_state[index]
