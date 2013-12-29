from singleton import Singleton
import wx
from random import randrange
from math import sqrt
from undo_stack import UndoStack

_DICT_ELEMS = [('results', None),
               ('clock', 0),
               ('first_circle', True),
               ('clock_pause', False),
               ('legend', None),
               ('title', "Graph"),
               ('dispW', 0),
               ('dispH', 0),
               ('max_time', 1),
               ('clock_increment', 1/600.0),
               ('parser', None),
               ('annotate', False),
               ('annotations', []),
               ('temp_annotation', None),
               ('annotation_mode', None),
               ('max_height', 0),
               ('annotation_text', ""),
               ('species_dict', {}),
               ('results', None),
               ('lines', {}),
               ('first_time', True),
               ('cell_segments', []),
               ('start_playing', False),
               ('click_one', False),
               ('click_one_x', 0),
               ('click_one_y', 0),
               ('attached_file_locations', []),
               ('draw_plot', None),
               ('xkcd', False),
               ('graph_canvas', None),
               ('redraw_legend', True),
               ('draw_annotations', True)]


@Singleton
class WorldState:

    def __init__(self):
        self._NONE = 0
        self._ARROW = 1
        self._TEXT = 2
        self._TEXT_ARROW = 3
        self._CIRCLE = 4
        self.colours = []
        self.hard_colours = self.populate_colours()
        self.undo_stack = UndoStack()

        self.session_dict = dict(_DICT_ELEMS)
        self.temp_session = None

    def reset_session(session_dict):
        for (key, value) in _DICT_ELEMS:
            session_dict[key] = value
        return session_dict

    def update_clock_increment(self):
        self.session_dict['clock_increment'] = self.session_dict['max_time'] / 600.0

    def change_cursor(self, cursor):
        self.session_dict['graph_canvas'].SetCursor(wx.StockCursor(cursor))

    def euclid_distance(self, p1, p2):
        return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

    """
    Work through the list of set colours first.  Then start generating new
    colours - if they are too close then regenerate
    """
    def choose_colour(self):
        if (len(self.hard_colours) > 0):
            return self.hard_colours.pop()
        else:
            accept = False

            while(not accept):
                accept = True
                temp_colour = self.random_colour()
                for colour in self.colours:
                    if (self.euclid_distance(temp_colour, colour) < 50):
                        accept = False
                        break
            self.colours.append(temp_colour)
            return temp_colour

    def random_colour(self):
        return (randrange(0, 200, 1),
                randrange(0, 200, 1),
                randrange(0, 200, 1))

    def populate_colours(self):
        return [(255, 0, 0),
                (0, 255, 0),
                (0, 0, 255)]

    def undo(self):
        self.session_dict = self.undo_stack.pop()

    def push_state(self):
        #TODO: Need to push a copy onto here
        self.undo_stack.push(self.session_dict.copy())
        print "$$$$$$$$$$$$$$$"
        for state in self.undo_stack.stack:
            print state['annotations']
