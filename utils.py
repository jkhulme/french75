from math import sqrt
import wx
from biopepa_csv_parser import BioPepaCsvParser
from worldstate import WorldState


world = WorldState.Instance()


def open_results_file(self):
    file_chooser = wx.FileDialog(
        self,
        message="Choose a file",
        wildcard="*.csv",
        style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR)
    if file_chooser.ShowModal() == wx.ID_OK:
        paths = file_chooser.GetPaths()
        results = {}
        parser = BioPepaCsvParser()
        for path in paths:
            parser.parse_csv(path)
            results[path.split('/')[-1]] = parser.results_dict

        world.session_dict['results'] = results
        world.session_dict['parser'] = parser

        file_chooser.Destroy()
    else:
        file_chooser.Destroy()

def rgb_to_hex(rgb):
    """
    Having trouble getting matplotlib to take an rgb tuple, so convert to hex which is working.
    Taken from this thread: http://stackoverflow.com/questions/214359/converting-hex-color-to-rgb-and-vice-versa
    """
    return '#%02x%02x%02x' % rgb


def euclid_distance(p1, p2):
    return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

def point_to_line_distance((l1_x, l1_y), (l2_x, l2_y), (p_x, p_y)):
    m = float(l2_y - l1_y)/float(l2_x - l1_x)
    a = -m
    b = 1
    c = l1_y - (m*l1_x)
    top = abs(a*p_x + b*p_y - c)
    bottom = sqrt(a**2 + b**2)
    return top/float(bottom)

def rgba_to_rgb((r, g, b), a):
    """
    Blend the colour of the line segment with the background - ration specified by
    alpha value.  This prevents the blending with the other line segment
    Taken from stack overflow:
    """
    bg = tuple([255 * (1 - a)] * 3)
    fg = (r * a, g * a, b * a)
    add_tuples = lambda (r1, g1, b1), (r2, g2, b2): (r1 + r2, g1 + g2, b1 + b2)
    return add_tuples(bg, fg)

def calc_graph_size(dpi, cols, num_sidebars, phi):
    graph_width = int(((world.session_dict['dispW'] / cols) * (cols - num_sidebars)) / dpi)
    graph_height = int(graph_width/phi)
    return (graph_width, graph_height)
