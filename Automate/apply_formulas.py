"""
~~~~~~~~~~~~~~~~~~~~~~~
Make a object to implement all the mathematical related functionality.
"""
import numpy


def add(first_value, next_value):
    """
    Defining the way to apply addition
    to the row or column data
    :param first_value: The first value that user wants to add with
    :param next_value: The next value that user wants to add with
    :return: numpy array
    """
    return numpy.array(first_value) + numpy.array(next_value)


def division(first_value, next_value):
    """
    Defining the way to apply division
    to the row or column data
    :param first_value: The value that user wants to divide with
    :param next_value: A int or object from which that user want to divide with
    :return: numpy array
    """
    return numpy.array(first_value) / numpy.array(next_value)


def multiplication(first_value, next_value):
    """
    Defining the way to apply multiplication
    to the row or column data
    :param first_value: First value that user wants to multiply with
    :param next_value: The next value that user wants to multiply with
    :return: numpy array
    """
    return numpy.array(first_value) * numpy.array(next_value)


def subtraction(first_value, next_value):
    """
    Defining the way to apply subtraction
    to the row or column data
    :param first_value: The first value that user wants to subtract with
    :param next_value: The next value that user wants to subtract with
    :return: numpy array
    """
    return numpy.array(first_value) - numpy.array(next_value)
