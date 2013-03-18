from biopepa_csv_parser import BioPepaCsvParser
from biopepa_model_parser import Biopepa_Model_Parser
from plotter import Plotter
import wx
import matplotlib
matplotlib.use('WXAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import \
    FigureCanvasWxAgg as FigCanvas, \
    NavigationToolbar2WxAgg as NavigationToolbar
from legend import Legend
import os


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
        self.dpi = 100
        self.results = {}
        self.first_time = True
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

        self.toolbar = NavigationToolbar(self.graph_canvas)
        self.toolbar.DeleteToolByPos(7)
        self.toolbar.DeleteToolByPos(6)
        self.toolbar.DeleteToolByPos(6)
        self.graph_vbox.Add(self.toolbar)

        self.graph_panel.SetSizer(self.graph_vbox)
        self.graph_vbox.Fit(self)

        self.legend = Legend(self.legend_panel)

        menubar = wx.MenuBar()
        file_menu = wx.Menu()
        filem = file_menu.Append(wx.ID_OPEN, '&Open')
        filem2 = file_menu.Append(wx.ID_ANY, '&View Model')
        file_save_plot = file_menu.Append(wx.ID_SAVE, '&Save')
        menubar.Append(file_menu, '&File')
        self.SetMenuBar(menubar)
        self.Bind(wx.EVT_MENU, self.open_file, filem)
        self.Bind(wx.EVT_MENU, self.open_file2, filem2)
        self.Bind(wx.EVT_MENU, self.on_save_plot, file_save_plot)

        self.splitter_two.SplitVertically(self.model_panel, self.splitter)
        self.splitter_two.SetSashPosition(200)

        self.splitter.SplitVertically(self.graph_panel, self.legend_panel)
        self.splitter.SetSashPosition(800)

        self.SetSize((1200, 540))
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
            style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR)
        if file_chooser.ShowModal() == wx.ID_OK:
            self.paths = file_chooser.GetPaths()
            file_chooser.Destroy()

            self.plot_graphs()
            self.model_panel.Parent.Refresh()
        else:
            file_chooser.Destroy()

    def open_file2(self, e):
        file_chooser = wx.FileDialog(
            self,
            message="Choose a file",
            wildcard="*.biopepa",
            style=wx.OPEN | wx.CHANGE_DIR)
        if file_chooser.ShowModal() == wx.ID_OK:
            self.paths = file_chooser.GetPaths()
            file_chooser.Destroy()

            self.model_parser = Biopepa_Model_Parser()
            self.model_parser.open_model(self.paths[0])
            self.model_parser.get_locations()
            self.model_parser.parse_location()
            self.model_parser.build_graph()

            self.model_panel.Bind(wx.EVT_PAINT, self.OnPaint)
            self.model_panel.Parent.Refresh()
            self.Show(False)
            self.Show(True)
        else:
            file_chooser.Destroy()

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
        self.draw_plot = Plotter(self.graph_axes, self.graph_canvas, self.results, self.parser, self.legend, True)
        self.draw_plot.plot()
        self.splitter.SetSashPosition(801)
        self.splitter.SetSashPosition(800)

    def OnPaint(self, e):
        dc = wx.PaintDC(self.model_panel)
        self.model_parser.tree.build_tree()
        if self.first_time:
            self.tree = self.model_parser.tree.draw_tree_one(dc)
            self.first_time = False
        else:
            self.tree = self.model_parser.tree.draw_tree_two(dc)

    def on_save_plot(self, event):
        file_choices = "PNG (*.png)|*.png"

        dlg = wx.FileDialog(
            self,
            message="Save plot as...",
            defaultDir=os.getcwd(),
            defaultFile="plot.png",
            wildcard=file_choices,
            style=wx.SAVE)

        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.draw_plot.mpl_legend = True
            self.draw_plot.plot()
            self.graph_canvas.print_figure(path, dpi=self.dpi)
            self.draw_plot.mpl_legend = False
            self.draw_plot.plot()


"""
Like Java's main method
"""
if __name__ == '__main__':
    app = wx.App()
    gui = French75(None)
    gui.Show()
    app.MainLoop()
