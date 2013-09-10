from math import sqrt

"""
Having trouble getting matplotlib to take an rgb tuple, so convert to hex which is working.
Taken from this thread: http://stackoverflow.com/questions/214359/converting-hex-color-to-rgb-and-vice-versa
"""
def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb

def euclid_distance(p1, p2):
    return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

"""
Blend the colour of the line segment with the background - ration specified by
alpha value.  This prevents the blending with the other line segment
Taken from stack overflow:
"""
def rgba_to_rgb((r,g,b), a):
    bg = tuple([255 * (1 - a)] * 3)
    fg = (r * a, g * a, b * a)
    add_tuples = lambda (r1,g1,b1), (r2, g2, b2) : (r1 + r2, g1 + g2, b1 + b2)
    return add_tuples(bg, fg)
