from numpy import interp
import math

def scale(number ,minRange, maxRange, scaledMinRange, scaledMaxRange):
    return math.floor(interp(number, [minRange, maxRange], [scaledMinRange, scaledMaxRange]))