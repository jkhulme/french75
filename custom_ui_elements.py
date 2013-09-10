from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg as NavigationToolbar


class BioPepaToolbar(NavigationToolbar):

    def __init__(self, graph_canvas):
        super(NavigationToolbar, self).__init__(graph_canvas)
        self.DeleteToolByPos(7)
        self.DeleteToolByPos(6)
        self.DeleteToolByPos(6)
