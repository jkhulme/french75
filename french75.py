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
import sys
import os

_DPI = 80
_BG_COLOUR = 'white'
_TITLE = 'French75'
_PHI = 1.618
_COLS = 6
_NUM_OF_SIDEBARS = 2


class French75(wx.Frame):

    """
    self.results - data to be plotted
    self.panel - container for the drawn graph
    self.graph_fig - container for the canvas
    self.graph_canvas - container where we draw the graph
    self.graph_axes - container that holds the data about what has been plotted
    self.graph_vbox - another layout container
    self.splitter_right - splits the windows
    self.graph_panel - where the standard graph is drawn
    self.model_panel - where the legend for the standard graph is drawn
    self.legend - what is drawn on the legend panel
    self.paths - all the files to be read
    self.parser - csv parser
    """

    def __init__(self, *args, **kwargs):
        super(French75, self).__init__(*args, **kwargs)
        self.first_time = True
        sys.argv = sys.argv[1:]
        for arg in sys.argv:
            if (arg == "--xkcd"):
                self.xkcd = True
                break
        else:
            self.xkcd = False

        self.launch_gui()

    """
    Draws the main window
    """
    def launch_gui(self):
        (dispW, dispH) = wx.DisplaySize()

        #the containers
        self.splitter_left = wx.SplitterWindow(self, -1)
        self.legend_panel = wx.Panel(self.splitter_left, -1)
        self.splitter_right = wx.SplitterWindow(self.splitter_left, -1)
        self.graph_panel = wx.Panel(self.splitter_right, -1)
        self.model_panel = wx.Panel(self.splitter_right, -1)

        self.model_panel.SetBackgroundColour(_BG_COLOUR)
        self.legend_panel.SetBackgroundColour(_BG_COLOUR)
        self.graph_panel.SetBackgroundColour(_BG_COLOUR)

        #graph stuff - This assumes a typical top or bottom status bar.
        #Systems with a side bar will not work with this
        graph_width = int(((dispW/_COLS)*(_COLS -_NUM_OF_SIDEBARS))/_DPI)
        graph_height = int(graph_width/_PHI)
        self.graph_fig = Figure((graph_width, graph_height))
        self.graph_fig.set_facecolor('white')
        self.graph_canvas = FigCanvas(self.graph_panel, -1, self.graph_fig)
        self.graph_axes = self.graph_fig.add_subplot(111)
        self.graph_vbox = wx.BoxSizer(wx.VERTICAL)
        self.graph_vbox.Add(self.graph_canvas)

        toolbar = self.build_tool_bar()
        self.graph_vbox.Add(toolbar)

        self.graph_panel.SetSizer(self.graph_vbox)
        self.graph_vbox.Fit(self)

        self.legend = Legend(self.legend_panel)

        self.SetMenuBar(self.build_menu_bar())

        self.splitter_left.SplitVertically(self.legend_panel, self.splitter_right)
        self.splitter_right.SplitVertically(self.graph_panel, self.model_panel)

        #Its purpose it to maximise the main window and then set the components
        #at the appropriate sizes - relative to total size
        self.Maximize()
        (self.winW, self.winH) = self.GetSize()
        self.splitter_left.SetSashPosition(self.winW/6)
        self.splitter_right.SetSashPosition(4 * self.winW/6)

        #Display everything
        self.SetTitle(_TITLE)
        self.Centre()
        self.Show(True)

    """
    Getting rid of the toolbar buttons that user doesn't need
    Could take this out to be its own class
    """
    def build_tool_bar(self):
        toolbar = NavigationToolbar(self.graph_canvas)
        toolbar.DeleteToolByPos(7)
        toolbar.DeleteToolByPos(6)
        toolbar.DeleteToolByPos(6)
        return toolbar

    """
    The menu bar.
    Again could take this out to be its own class
    Need to organise the menu a bit better - look at mac style guidelines
    """
    def build_menu_bar(self):
        menubar = wx.MenuBar()
        menubar.SetBackgroundColour(_BG_COLOUR)

        file_menu = wx.Menu()
        filem_open_results = file_menu.Append(wx.ID_OPEN, '&Open')
        filem_open_results_save_plot = file_menu.Append(wx.ID_SAVE, '&Save')
        file_menu.AppendSeparator()
        filem_open_results_open_model = file_menu.Append(wx.ID_ANY, '&View Model')
        filem_open_results_save_model = file_menu.Append(wx.ID_ANY, 'Save &Model')

        menubar.Append(file_menu, '&File')

        self.Bind(wx.EVT_MENU, self.open_results_file, filem_open_results)
        self.Bind(wx.EVT_MENU, self.open_model_file, filem_open_results_open_model)
        self.Bind(wx.EVT_MENU, self.save_snapshot, filem_open_results_save_model)
        self.Bind(wx.EVT_MENU, self.on_save_plot, filem_open_results_save_plot)

        return menubar

    """
    selects which csv files to use
    """
    def open_results_file(self, e):
        file_chooser = wx.FileDialog(
            self,
            message="Choose a file",
            wildcard="*.csv",
            style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR)
        if file_chooser.ShowModal() == wx.ID_OK:
            self.paths = file_chooser.GetPaths()
            file_chooser.Destroy()

            self.plot_graphs()
            self.legend_panel.Parent.Refresh()
        else:
            file_chooser.Destroy()

    """
    Which biopepa model to display
    """
    def open_model_file(self, e):
        file_chooser = wx.FileDialog(
            self,
            message="Choose a file",
            wildcard="*.biopepa",
            style=wx.OPEN | wx.CHANGE_DIR)
        if file_chooser.ShowModal() == wx.ID_OK:
            self.paths = file_chooser.GetPaths()
            file_chooser.Destroy()

            self.model_parser = Biopepa_Model_Parser()
            self.model_parser.parse(self.paths[0])
            self.model_parser.build_graph()

            self.refresh_legend_panel()
        else:
            file_chooser.Destroy()

    def refresh_legend_panel(self):
        self.model_panel.Bind(wx.EVT_PAINT, self.on_paint)
        self.model_panel.Parent.Refresh()
        self.Show(False)
        self.Show(True)

    """
    Get the data then plot it
    """
    def plot_graphs(self):
        results = {}
        parser = BioPepaCsvParser()
        for path in self.paths:
            parser.parse_csv(path)
            results[path.split('/')[-1]] = parser.results_dict
        self.draw_plot = Plotter(self.graph_axes, self.graph_canvas, results, parser, self.legend, True, self.xkcd)
        self.draw_plot.plot()
        self.splitter_left.SetSashPosition(self.splitter_left.GetSashPosition() + 1)
        self.splitter_left.SetSashPosition(self.splitter_left.GetSashPosition() - 1)

    """
    Handles drawing of the model
    """
    def on_paint(self, e):
        self.dc = wx.PaintDC(self.model_panel)
        if self.first_time:
            self.model_parser.tree.build_tree()
            self.tree = self.model_parser.tree.draw_tree_one(self.dc)
            self.first_time = False
        else:
            self.tree = self.model_parser.tree.draw_tree_one(self.dc)

    """
    Save the graph
    """
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
    Save a picture of the model
    based largely on code posted to wxpython-users by Andrea Gavana 2006-11-08
    """
    def save_snapshot(self, e):
        dcSource = self.dc
        size = dcSource.Size
        bmp = wx.EmptyBitmap(200, 200)
        memDC = wx.MemoryDC()
        memDC.SelectObject(bmp)
        memDC.Blit(0, 0, size.width, size.height, dcSource, 0, 0)
        memDC.SelectObject(wx.NullBitmap)
        img = bmp.ConvertToImage()
        img.SaveFile('saved.png', wx.BITMAP_TYPE_PNG)

if __name__ == '__main__':
    app = wx.App()
    gui = French75(None)
    gui.Show()
    app.MainLoop()
