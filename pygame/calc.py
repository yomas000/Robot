import math

def moveIteration(number) -> int:
    """
    number: [int] - This is your x value to pass into the graphing function

    returns: [int] - the y value of the graph from 1 - 20
    """
    return (6 * math.log(number)) + 6