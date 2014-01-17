from singleton import Singleton
import wx
from random import randrange
from math import sqrt
from undo_stack import UndoStack
import copy
import pickle


_DICT_ELEMS = [('results', None),
               ('clock', 0),
               ('first_circle', True),
               ('clock_pause', False),
               ('title', "Graph"),
               ('dispW', 0),
               ('dispH', 0),
               ('max_time', 1),
               ('clock_increment', 1/600.0),
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
               ('start_playing', False),
               ('click_one', False),
               ('click_one_x', 0),
               ('click_one_y', 0),
               ('attached_file_locations', []),
               ('xkcd', False),
               ('redraw_legend', True),
               ('draw_annotations', True),
               ('ymin', 0),
               ('ymax', 0),
               ('xmin', 0),
               ('xmax', 0),
               ('tree_list', None),
               ('graph_width', 0),
               ('graph_height', 0),
               ('normalised', False)]

_DICT_RESET = [('results', None),
               ('clock', 0),
               ('first_circle', True),
               ('clock_pause', False),
               ('title', "Graph"),
               #('dispW', 0),
               #('dispH', 0),
               ('max_time', 1),
               ('clock_increment', 1/600.0),
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
               ('start_playing', False),
               ('click_one', False),
               ('click_one_x', 0),
               ('click_one_y', 0),
               ('attached_file_locations', []),
               ('xkcd', False),
               ('redraw_legend', True),
               ('draw_annotations', True),
               ('ymin', 0),
               ('ymax', 0),
               ('xmin', 0),
               ('xmax', 0),
               ('tree_list', None),
               #('graph_width', 0),
               #('graph_height', 0),
               ('normalised', False)]


@Singleton
class WorldState:

    """
    Singleton for sharing data between different parts of the program.  Saves having to keep track of where everything has been passed
    """

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
        self.graph_axes = None
        self.legend = None
        self.parser = None
        self.draw_plot = None
        self.cell_segments = []
        self.graph_canvas = None

    def reset_session(self, session_dict):
        """
        Set everything back to a default value
        """
        for (key, value) in _DICT_RESET:
            session_dict[key] = value
        return session_dict

    def update_clock_increment(self):
        """
        Current update rate is set for 1 minute run time
        """
        self.session_dict['clock_increment'] = self.session_dict['max_time'] / 600.0

    def change_cursor(self, cursor):
        self.graph_canvas.SetCursor(wx.StockCursor(cursor))

    def euclid_distance(self, p1, p2):
        """
        Had to have this here so that deep copying the dictionary in the undo
        stack would keep working
        """
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
        """
        The 50 closest to white are skipped to prevent pale colours
        """
        return (randrange(0, 200, 1),
                randrange(0, 200, 1),
                randrange(0, 200, 1))

    def populate_colours(self):
        """
        Default list: red, blue and green
        """
        return [(255, 0, 0),
                (0, 255, 0),
                (0, 0, 255)]

    def undo(self):
        """
        Need to update values one by one because some need to be taken out
        of the session dict <- TODO
        """
        try:
          self.session_dict = self.undo_stack.undo_pop()
        except:
          pass

    def redo(self):
        self.session_dict = self.undo_stack.redo_pop()

    def push_state(self):
        """
        Put the current session dict onto the undo stack, change the title to
        indicate that there are unsaved changes.  Need to copy some values
        across for the same reason as undo.

        Need to use deepcopy so that objects in the dictionary are not just
        references
        """
        self.update_title("French75 - Unsaved Changes")
        self.undo_stack.undo_push(copy.deepcopy(self.session_dict))

    def pickle_session(self):
        """
        serialize the data, currently just going to be for saving and loading
        sessions but it could be used to for the concurrency stuff as well.
        """
        return pickle.dumps(self.session_dict)

    def unpickle_session(self, data):
        """
        Deserialize the data, just replaces the session dict as that is where
        the important stuff is
        """
        self.session_dict = pickle.loads(data)
