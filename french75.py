from biopepa_csv_parser import BioPepaCsvParser
from biopepa_model_parser import Biopepa_Model_Parser
from plotter import Plotter
import wx
import matplotlib
matplotlib.use('WXAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigCanvas
from legend import Legend
#from draw_model import ModelVis


class French75(wx.Frame):

    """
    self.results - data to be plotted
    self.panel - container for the drawn graph
    self.graph_fig - container for the canvas
    self.graph_canvas - container where we draw the graph
    self.graph_axes - container that holds the data about what has been plotted
    self.graph_vbox - another layout container
    self.splitter - splits the windows
    self.graph_panel - where the standard graph is drawn
    self.legend_panel - where the legend for the standard graph is drawn
    self.legend - what is drawn on the legend panel
    self.paths - all the files to be read
    self.parser - csv parser
    """

    def __init__(self, *args, **kwargs):
        super(French75, self).__init__(*args, **kwargs)

        self.results = {}
        self.launch_gui()

    """
    Draws the main window
    """
    def launch_gui(self):
        self.splitter_two = wx.SplitterWindow(self,)
        self.model_panel = wx.Panel(self.splitter_two, -1)
        self.splitter = wx.SplitterWindow(self.splitter_two, -1)
        self.graph_panel = wx.Panel(self.splitter, -1)
        self.legend_panel = wx.Panel(self.splitter, -1)

        self.graph_fig = Figure((10.0, 6))
        self.graph_canvas = FigCanvas(self.graph_panel, -1, self.graph_fig)
        self.graph_axes = self.graph_fig.add_subplot(111)

        self.graph_vbox = wx.BoxSizer(wx.VERTICAL)
        self.graph_vbox.Add(self.graph_canvas)
        self.graph_panel.SetSizer(self.graph_vbox)
        self.graph_vbox.Fit(self)

        self.legend = Legend(self.legend_panel)

        menubar = wx.MenuBar()
        file_menu = wx.Menu()
        filem = file_menu.Append(wx.ID_OPEN, '&Open')
        menubar.Append(file_menu, '&File')
        self.SetMenuBar(menubar)
        self.Bind(wx.EVT_MENU, self.open_file, filem)

        self.splitter_two.SplitVertically(self.model_panel, self.splitter)
        self.splitter_two.SetSashPosition(200)

        self.splitter.SplitVertically(self.graph_panel, self.legend_panel)
        self.splitter.SetSashPosition(800)

        self.SetSize((1200, 500))
        self.SetTitle('French75')
        self.Centre()
        self.Show(True)

        self.model_panel.Bind(wx.EVT_PAINT, self.OnPaint)

        self.parser = Biopepa_Model_Parser()
        self.parser.open_model('camp-pka-mapk.biopepa')
        self.parser.get_locations()
        self.parser.parse_location()
        self.parser.build_graph()

    """
    selects which csv files to use
    """
    def open_file(self, e):
        file_chooser = wx.FileDialog(
            self,
            message="Choose a file",
            wildcard="*.csv",
            style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR
            )
        if file_chooser.ShowModal() == wx.ID_OK:
            self.paths = file_chooser.GetPaths()
        file_chooser.Destroy()

        self.plot_graphs()

    """
    Get the data then plot it
    """
    def plot_graphs(self):
        self.results = {}
        self.parser = BioPepaCsvParser()
        for path in self.paths:
            self.parser.open_csv(path)
            self.parser.parse_results()
            self.results[path.split('/')[-1]] = self.parser.results_dict
            self.parser.timescale()
        draw_plot = Plotter(self.graph_axes, self.graph_canvas, self.results, self.parser, self.legend, True)
        draw_plot.plot()
        self.splitter.SetSashPosition(801)
        self.splitter.SetSashPosition(800)

    def OnPaint(self, e):
        self.parser.tree.build_tree()
        self.tree = self.parser.tree.draw_tree()
        dc = wx.PaintDC(self.model_panel)
        for node in self.tree:
            if (self.parser.loc_results[node].l_type == 'membrane'):
                dc.DrawCircle(100, 100, 90)
        dc.SetBrush(wx.Brush('#004fc5'))
        for node in self.tree:
            if (self.parser.loc_results[node].parent == 'root'):
                dc.DrawCircle(100, 100, 60)

"""
Like Java's main method
"""
if __name__ == '__main__':
    app = wx.App()
    gui = French75(None)
    gui.Show()
    app.MainLoop()
