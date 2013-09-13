from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg as NavigationToolbar
from matplotlib.backends.backend_wx import _load_bitmap
import wx


class BioPepaToolbar(NavigationToolbar):

    ON_CUSTOM_ENLARGE = wx.NewId()
    #None is the separators
    toolitems = [t for t in NavigationToolbar.toolitems if t[0] in ('Home', 'Pan', 'Zoom', 'Back', 'Forward', None)]


    def __init__(self, graph_canvas):
        super(BioPepaToolbar, self).__init__(graph_canvas)
        self.AddSimpleTool(self.ON_CUSTOM_ENLARGE, _load_bitmap('stock_left.xpm'), 'Pan to the left', 'Pan graph to the left')
        wx.EVT_TOOL(self, self.ON_CUSTOM_ENLARGE, self._on_custom_enlarge)

    def _on_custom_enlarge(self, e):
        print "zoom and enhance."
