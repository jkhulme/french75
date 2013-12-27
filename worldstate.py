from singleton import Singleton
import wx

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
               ('redraw_legend', True)]


@Singleton
class WorldState:

    def __init__(self):
        self._NONE = 0
        self._ARROW = 1
        self._TEXT = 2
        self._TEXT_ARROW = 3
        self._CIRCLE = 4

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
