from biopepa_csv_parser import BioPepaCsvParser
from plotter import Plotter
import wx
import matplotlib
matplotlib.use('WXAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigCanvas
from legend import Legend


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
        self.splitter = wx.SplitterWindow(self, -1)
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

        self.splitter.SplitVertically(self.graph_panel, self.legend_panel)
        self.splitter.SetSashPosition(800)

        self.SetSize((1000, 500))
        self.SetTitle('French75')
        self.Centre()
        self.Show(True)

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
            self.parser.openCsv(path)
            self.parser.parseResults()
            self.results[path.split('/')[-1]] = self.parser.results_dict
            self.parser.timeScale()
        draw_plot = Plotter(self.graph_axes, self.graph_canvas, self.results, self.parser, self.legend)
        draw_plot.plot(True)


"""
Like Java's main method
"""
if __name__ == '__main__':
    app = wx.App()
    gui = French75(None)
    gui.Show()
    app.MainLoop()
