from biopepa_csv_parser import BioPepaCsvParser
from plotter import Plotter
#from gui_launcher import VisWindow
#import sys
import wx
import matplotlib
matplotlib.use('WXAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigCanvas


#results - one index for each csv file, dictionary of dictionaries
#argv - files passed to plotted

"""
results = {}
argv = sys.argv[1:]
"""


class French75(wx.Frame):

    def __init__(self, *args, **kwargs):
        super(French75, self).__init__(*args, **kwargs)
        self.results = {}
        self.launchGui()

    def launchGui(self):
        self.panel = wx.Panel(self)
        self.fig = Figure((5.0, 4.0))
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

        self.SetSize((500, 300))
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
        draw_plot = Plotter(self.axes, self.canvas)
        #draw_plot.draw_figure()
        draw_plot.plot(self.results, parser)
        #subs = draw_plot.build_colour_plot_arrays([1, 2, 3, 4, 5, 6], 2)
        #draw_plot.plot_colour_int(subs)

"""
Like Java's main method
"""
if __name__ == '__main__':
    app = wx.App()
    gui = French75(None)
    gui.Show()
    app.MainLoop()
