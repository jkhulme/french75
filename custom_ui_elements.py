from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg as NavigationToolbar
from matplotlib.backends.backend_wx import _load_bitmap
import wx
import platform
from worldstate import WorldState
from large_plot import LargePlotDialog


class BioPepaToolbar(NavigationToolbar):

    ON_CUSTOM_ENLARGE = wx.NewId()

    if (platform.system() != "Linux"):
        #None is for the separators
        toolitems = [t for t in NavigationToolbar.toolitems if t[0] in ('Home', 'Pan', 'Zoom', 'Back', 'Forward', None)]

    def __init__(self, graph_canvas):
        super(BioPepaToolbar, self).__init__(graph_canvas)
        self.world = WorldState.Instance()
        if (platform.system() == "Linux"):
            #save
            self.DeleteToolByPos(8)
            #subplots
            self.DeleteToolByPos(7)
        self.AddSimpleTool(self.ON_CUSTOM_ENLARGE, _load_bitmap('stock_left.xpm'), 'Pan to the left', 'Pan graph to the left')
        wx.EVT_TOOL(self, self.ON_CUSTOM_ENLARGE, self._on_custom_enlarge)

    def _on_custom_enlarge(self, e):
        large_plot = LargePlotDialog(None, title='Big Plot')
        large_plot.ShowModal()
        large_plot.Destroy()
