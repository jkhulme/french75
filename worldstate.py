from singleton import Singleton


@Singleton
class WorldState:

    def __init__(self):
        print "World created"
        self.results = None
