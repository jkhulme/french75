from biopepa_csv_parser import BioPepaCsvParser
from plotter import Plotter
import wx
import matplotlib
matplotlib.use('WXAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigCanvas
from legend import Legend


class French75(wx.Frame):

    #self.results - data to be plotted
    #self.panel - container for the drawn graph
    #self.fig - container for the canvas
    #self.canvas - container where we draw the graph
    #self.axes - container that holds the data about what has been plotted
    #self.vbox - another layout container

    def __init__(self, *args, **kwargs):
        super(French75, self).__init__(*args, **kwargs)
        self.results = {}
        self.launchGui()

    def launchGui(self):
        self.splitter = wx.SplitterWindow(self, -1)
        self.graph_panel = wx.Panel(self.splitter, -1)
        self.legend_panel = wx.Panel(self.splitter, -1)

        self.fig = Figure((10.0, 6))
        self.canvas = FigCanvas(self.graph_panel, -1, self.fig)
        self.axes = self.fig.add_subplot(111)
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.vbox.Add(self.canvas)
        self.graph_panel.SetSizer(self.vbox)
        self.vbox.Fit(self)

        self.legend = Legend(self.legend_panel)
        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        filem = fileMenu.Append(wx.ID_OPEN, '&Open')
        menubar.Append(fileMenu, '&File')
        self.SetMenuBar(menubar)
        self.splitter.SplitVertically(self.graph_panel, self.legend_panel)
        self.splitter.SetSashPosition(800)
        self.Bind(wx.EVT_MENU, self.openFile, filem)
        self.SetSize((1000, 500))
        self.SetTitle('French75')
        self.Centre()
        self.Show(True)

    def openFile(self, e):
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

    def plot_graphs(self):
        self.results = {}
        parser = BioPepaCsvParser()
        for path in self.paths:
            parser.openCsv(path)
            parser.parseResults()
            self.results[path] = parser.results_dict
            parser.timeScale()
        draw_plot = Plotter(self.axes, self.canvas, self.results, parser, self.legend)
        draw_plot.plot()
        #draw_plot.plot_colour_int()


"""
Like Java's main method
"""
if __name__ == '__main__':
    app = wx.App()
    gui = French75(None)
    gui.Show()
    app.MainLoop()
