from math import sqrt

"""
Having trouble getting matplotlib to take an rgb tuple, so convert to hex which is working.
Taken from this thread: http://stackoverflow.com/questions/214359/converting-hex-color-to-rgb-and-vice-versa
"""


def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb


def euclid_distance(p1, p2):
    return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)
