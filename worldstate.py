from singleton import Singleton


@Singleton
class WorldState:

    def __init__(self):
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
