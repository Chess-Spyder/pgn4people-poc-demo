""" Utilities more general than those found in more-targeted utility modules """


def is_even_number(number):
    """
    Returns true iff argument is an even number
    """
    return (number % 2) == 0


def is_odd_number(number):
    """
    Returns true iff argument is an odd number
    """
    return (number % 2) != 0
