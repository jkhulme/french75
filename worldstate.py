from singleton import Singleton
import wx
from random import randrange
from math import sqrt
from undo_stack import UndoStack
import copy
import pickle
from method_sink import Sink
from singleton2 import SingletonMixin


_DICT_ELEMS = [('results', None),
               ('clock', 0),
               ('first_circle', True),
               ('clock_pause', False),
               ('title', "Graph"),
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
               ('normalised', False),
               ('annotate_anime', False),
               ('anime_annotations', {}),
               ('cur_annotation_id', 0)]

#@Singleton
#class WorldState:
class WorldState(SingletonMixin):

    """
    Singleton for sharing data between different parts of the program.  Saves having to keep track of where everything has been passed
    """

    def __init__(self):
        self._NONE = 0
        self._ARROW = 1
        self._TEXT = 2
        self._TEXT_ARROW = 3
        self._CIRCLE = 4
        self.dispW = 0
        self.dispH = 0
        self.graph_height = 0
        self.graph_height = 0

        self.colours = []
        self.hard_colours = self.populate_colours()

        self.undo_stack = UndoStack()

        self.session_dict = dict(_DICT_ELEMS)

        self.anime_annotations_list = None

        self.temp_session = None
        self.graph_axes = None
        self.legend = None
        self.parser = None
        self.draw_plot = None
        self.cell_segments = []
        self.graph_canvas = None

        self.server = Sink()
        self.client = Sink()

        self.panels = []

        self.lamport_clock = 0

    def reset_session(self):
        """
        Set everything back to a default value
        """
        for (key, value) in _DICT_ELEMS:
            self.session_dict[key] = value

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

    def choose_colour(self):
        """
        Work through the list of set colours first.  Then start generating new
        colours - if they are too close then regenerate
        """
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
        try:
            self.session_dict = self.undo_stack.undo_pop()
            self.legend.draw_legend()
            self.refresh_plot()
            for panel in self.panels:
                panel.Refresh()
            self.populate_anime_annotation_lb()
        except:
            print "*****UNDO FAILED*****"


    def redo(self):
        try:
            self.session_dict = self.undo_stack.redo_pop()
            self.legend.draw_legend()
            self.refresh_plot()
            for panel in self.panels:
                panel.Refresh()
            self.populate_anime_annotation_lb()
        except:
            print "*****REDO FAILED*****"

    def push_state(self, clock=None):
        """
        Put the current session dict onto the undo stack, change the title to
        indicate that there are unsaved changes.  Need to copy some values
        across for the same reason as undo.

        Need to use deepcopy so that objects in the dictionary are not just
        references
        """
        if clock is None:
            clock = self.lamport_clock
        self.update_title("French75 - Unsaved Changes")
        self.undo_stack.undo_push(copy.deepcopy((clock, self.session_dict)))

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

    def delete_annotation(self, a_id):
        new_annotation_list = [annotation for annotation in self.session_dict['annotations'] if annotation.id != a_id]
        self.session_dict['annotations'] = new_annotation_list
        self.refresh_plot()

    def refresh_plot(self):
        """
        Null pointers on the mac if I don't tell it to not redraw the legend
        unless necessary.
        """
        self.session_dict['redraw_legend'] = False
        self.draw_plot.plot()
        self.session_dict['redraw_legend'] = True

    def delete_anime_annotation(self, a_id):
        for key in self.session_dict['anime_annotations'].keys():
            new_annotation_list = [ann for ann in self.session_dict['anime_annotations'][key] if int(a_id) != int(ann.a_id)]
            self.session_dict['anime_annotations'][key] = new_annotation_list

        self.populate_anime_annotation_lb()

        for panel in self.panels:
            panel.Refresh()

    def add_anime_annotation(self, idx, annotation):
        self.set_time(annotation.start)
        if idx not in self.session_dict['anime_annotations'].keys():
            self.session_dict['anime_annotations'][idx] = [annotation]
        else:
            self.session_dict['anime_annotations'][idx].append(annotation)

        self.populate_anime_annotation_lb()

        for panel in self.panels:
            panel.Refresh()

    def update_annotation_text(self, a_id, text):
        for annotation in self.session_dict['annotations']:
            if annotation.id == a_id:
                annotation.text = text
                if annotation.type == self._ARROW:
                    annotation.type = self._TEXT_ARROW
                break
        self.refresh_plot()

    def populate_anime_annotation_lb(self):
        self.anime_annotations_list.Clear()
        for key in self.session_dict['anime_annotations'].keys():
            for annotation in self.session_dict['anime_annotations'][key]:
                self.anime_annotations_list.InsertItems([str(annotation.idx) + ": " + annotation.text], 0)

    def set_time(self, time):
        self.session_dict['clock'] = time
        self.time_slider.SetValue(self.session_dict['clock'])
        self.refresh_plot()
        for panel in self.panels:
                panel.Refresh()

    def switch_animation(self, n):
        if self.drop_down_species.IsEnabled():
            self.drop_down_species.Enable(False)
            self.drop_down_files.Enable(True)
            self.create_cell_segments_by_species(n)
        else:
            self.drop_down_species.Enable(True)
            self.drop_down_files.Enable(False)
            self.create_cell_segments_by_file(n)

    def reorder(self, clock):
        """
        This is used mainly for distributed mode, ensuring that
        everyone sees in the same order.  Lost in non blocking communication
        """
        self.push_state(clock)
        self.session_dict = self.undo_stack.reorder()
        self.refresh_plot()
        self.refresh_animation()

    def refresh_animation(self):
        for panel in self.panels:
            panel.Refresh()
