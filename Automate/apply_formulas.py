"""
--------------------------------------------------------->
Copyrights (c) to UR's tech.ltd 2021. All rights reserved
Author: Uday lal
company: UR's tech.ltd
--------------------------------------------------------->

~~~~~~~~~~~~~~~~~~~~~~~
Make a object to implement all the mathematical related functionality.
"""
import numpy


class ApplyFormulas:
    def __init__(self, data):
        self.data = numpy.array(data)

    def add(self, next_value):
        """
        Defining the way to apply addition
        to the row or column data
        :param next_value: The next value that user wants to add with
        :return: numpy array
        """
        return self.data + numpy.array(next_value)

    def division(self, next_value):
        """
        Defining the way to apply division
        to the row or column data
        :param next_value: A int or object from which that user want to divide with
        :return: numpy array
        """
        return self.data / numpy.array(next_value)

    def multiplication(self, next_value):
        """
        Defining the way to apply multiplication
        to the row or column data
        :param next_value: The next value that user wants to multiply with
        :return: numpy array
        """
        return self.data * numpy.array(next_value)

    def subtraction(self, next_value):
        """
        Defining the way to apply subtraction
        to the row or column data
        :param next_value: The next value that user wants to subtract with
        :return: numpy array
        """
        return self.data - numpy.array(next_value)
