from biopepa_csv_parser import BioPepaCsvParser
from plotter import Plotter
import wx
import matplotlib
matplotlib.use('WXAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigCanvas


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
        self.panel = wx.Panel(self)
        self.fig = Figure((10.0, 6))
        self.canvas = FigCanvas(self.panel, -1, self.fig)
        self.axes = self.fig.add_subplot(111)
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.vbox.Add(self.canvas)
        self.panel.SetSizer(self.vbox)
        self.vbox.Fit(self)
        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        filem = fileMenu.Append(wx.ID_OPEN, '&Open')
        menubar.Append(fileMenu, '&File')
        self.SetMenuBar(menubar)

        self.Bind(wx.EVT_MENU, self.openFile, filem)

        self.SetSize((800, 500))
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
        draw_plot = Plotter(self.axes, self.canvas, self.results, parser)
        #draw_plot.plot()
        draw_plot.plot_colour_int()

"""
Like Java's main method
"""
if __name__ == '__main__':
    app = wx.App()
    gui = French75(None)
    gui.Show()
    app.MainLoop()
