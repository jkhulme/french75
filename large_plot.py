import wx
import matplotlib
matplotlib.use('WXAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigCanvas, NavigationToolbar2WxAgg as NavigationToolbar
from plotter import Plotter
from worldstate import WorldState

_BG_COLOUR = 'white'
_COLS = 6
_NUM_OF_SIDEBARS = 2
_DPI = 80
_PHI = 1.618

class LargePlotDialog(wx.Dialog):

    def __init__(self, *args, **kw):
        super(LargePlotDialog, self).__init__(*args, **kw)
        #WorldState.Instance() = WorldState.Instance()
        graph_panel = wx.Panel(self, -1)
        graph_panel.SetBackgroundColour(_BG_COLOUR)
        graph_width = int((WorldState.Instance().dispW - 10) / _DPI)
        graph_height = int(graph_width/_PHI)
        graph_fig = Figure((graph_width, graph_height))
        graph_fig.set_facecolor('white')
        self.graph_canvas = FigCanvas(graph_panel, -1, graph_fig)
        self.graph_axes = graph_fig.add_subplot(111)
        graph_vbox = wx.BoxSizer(wx.VERTICAL)
        graph_vbox.Add(self.graph_canvas)
        toolbar = NavigationToolbar(self.graph_canvas)
        graph_vbox.Add(toolbar)
        graph_panel.SetSizer(graph_vbox)
        graph_vbox.Fit(self)
        self.SetSize((WorldState.Instance().dispW - 10, ((WorldState.Instance().dispW) / _PHI) + 50))
        self.Centre()
        self.draw_plot = Plotter(self.graph_axes)
        self.draw_plot.mpl_legend = True
        self.draw_plot.plot()
