from singleton import Singleton
import wx


@Singleton
class WorldState:

    def __init__(self):
        self._NONE = 0
        self._ARROW = 1
        self._TEXT = 2
        self._TEXT_ARROW = 3
        self._CIRCLE = 4

        self.results = None
        self.clock = 0
        self.first_circle = True
        self.clock_pause = False
        self.legend = None
        self.title = "Graph"
        self.dispW = 0
        self.dispH = 0
        self.max_time = 1
        self.clock_increment = self.max_time / 600.0
        self.parser = None
        self.annotate = False
        self.annotations = []

    def update_clock_increment(self):
        self.clock_increment = self.max_time / 600.0

    def change_cursor(self, cursor):
        self.graph_canvas.SetCursor(wx.StockCursor(cursor))
