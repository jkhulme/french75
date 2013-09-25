from biopepa_csv_parser import BioPepaCsvParser
from biopepa_model_parser import Biopepa_Model_Parser
from plotter import Plotter
import wx
import matplotlib
matplotlib.use('WXAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigCanvas
from legend import Legend
import sys
import os
from custom_ui_elements import BioPepaToolbar
from session_creator import SessionDialog
from worldstate import WorldState
from cell_segment import CellSegment
import time
from threading import Thread

_DPI = 80
_BG_COLOUR = 'white'
_TITLE = 'French75'
_PHI = 1.618
_COLS = 6
_NUM_OF_SIDEBARS = 2


class French75(wx.Frame):

    """
    self.graph_canvas - container where we draw the graph
    self.graph_axes - container that holds the data about what has been plotted
    self.model_panel - where the legend for the standard graph is drawn
    self.legend - what is drawn on the legend panel
    self.paths - all the files to be read
    self.splitter_left - where the legend goes
    self.legend_panel - panel the legend goes on
    self.dc - drawing context
    self.draw_plot - the plotter which we use to draw lines
    self.dice - it was lying about screen res - so check for it
    """

    def __init__(self, *args, **kwargs):
        super(French75, self).__init__(*args, **kwargs)
        self.world = WorldState.Instance()
        self.world.clock = 0
        self.first_time = True
        self.parse_args()
        (dispW, dispH) = self.get_resolution()
        self.world.first_circle = True

        self.splitter_left = wx.SplitterWindow(self, -1)
        self.legend_panel = wx.Panel(self.splitter_left, -1)
        splitter_right = wx.SplitterWindow(self.splitter_left, -1)
        splitter_middle = wx.SplitterWindow(splitter_right)
        graph_panel = wx.Panel(splitter_middle, -1)
        self.model_panel = wx.Panel(splitter_right, -1)
        self.animation_panel = wx.Panel(splitter_middle, -1)

        self.model_panel.SetBackgroundColour(_BG_COLOUR)
        self.legend_panel.SetBackgroundColour(_BG_COLOUR)
        graph_panel.SetBackgroundColour(_BG_COLOUR)
        self.animation_panel.SetBackgroundColour(_BG_COLOUR)

        graph_width = int(((dispW / _COLS) * (_COLS - _NUM_OF_SIDEBARS)) / _DPI)
        graph_height = int(graph_width/_PHI)
        graph_fig = Figure((graph_width, graph_height))

        graph_fig.set_facecolor('white')

        self.graph_canvas = FigCanvas(graph_panel, -1, graph_fig)
        self.graph_axes = graph_fig.add_subplot(111)
        graph_vbox = wx.BoxSizer(wx.VERTICAL)
        graph_vbox.Add(self.graph_canvas)
        toolbar = BioPepaToolbar(self.graph_canvas)
        (toolW, toolH) = toolbar.GetSizeTuple()
        graph_vbox.Add(toolbar)
        graph_panel.SetSizer(graph_vbox)
        graph_vbox.Fit(self)

        self.legend = Legend(self.legend_panel)
        self.world.legend = self.legend
        self.SetMenuBar(self.build_menu_bar())

        self.splitter_left.SplitVertically(self.legend_panel, splitter_right)
        splitter_right.SplitVertically(splitter_middle, self.model_panel)
        splitter_middle.SplitHorizontally(graph_panel, self.animation_panel)

        self.Maximize()
        self.splitter_left.SetSashPosition(dispW/6)
        splitter_right.SetSashPosition(4 * dispW/6)
        splitter_middle.SetSashPosition((graph_height * _DPI) + toolH)
        self.SetTitle(_TITLE)
        self.Centre()
        self.Show(True)

    """
    currently only checks the xkcd parameter which is basically an easter egg - maybe there will be
    more at some point
    """
    def parse_args(self):
        sys.argv = sys.argv[1:]
        for arg in sys.argv:
            if (arg == "--xkcd"):
                matplotlib.pyplot.xkcd()
                self.xkcd = True
                break
        else:
            self.xkcd = False

    """
    because of cases where there are multiple monitors we need to go through
    all the monitors and decide which one to use - base this on mouse position.
    n/b - self.GetSize() might need to be used
    """
    def get_resolution(self):
        for monitor in [wx.Display(i) for i in range(wx.Display.GetCount())]:
            (dispW, dispH) = monitor.GetGeometry().GetSize()
            (mouseX, mouseY) = wx.GetMousePosition()
            if (mouseX < dispW):
                return (dispW, dispH)

    """
    The menu bar.
    Again could take this out to be its own class
    Need to organise the menu a bit better - look at mac style guidelines
    """
    def build_menu_bar(self):
        menubar = wx.MenuBar()
        menubar.SetBackgroundColour(_BG_COLOUR)

        file_menu = wx.Menu()
        filem_new_session = file_menu.Append(wx.ID_NEW, '&New Session')
        file_menu.AppendSeparator()
        filem_open_results = file_menu.Append(wx.ID_OPEN, '&Open')
        filem_open_results_save_plot = file_menu.Append(wx.ID_SAVE, '&Save')
        file_menu.AppendSeparator()
        filem_open_results_open_model = file_menu.Append(wx.ID_ANY, '&View Model')
        filem_open_results_save_model = file_menu.Append(wx.ID_ANY, 'Save &Model')

        menubar.Append(file_menu, '&File')

        self.Bind(wx.EVT_MENU, self.new_session, filem_new_session)
        self.Bind(wx.EVT_MENU, self.open_results_file, filem_open_results)
        self.Bind(wx.EVT_MENU, self.open_model_file, filem_open_results_open_model)
        self.Bind(wx.EVT_MENU, self.save_snapshot, filem_open_results_save_model)
        self.Bind(wx.EVT_MENU, self.on_save_plot, filem_open_results_save_plot)

        return menubar

    """
    Session starter dialogue
    """
    def new_session(self, e):
        session_dialog = SessionDialog(None, title='Session Starter')
        session_dialog.ShowModal()
        session_dialog.Destroy()

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
            paths = file_chooser.GetPaths()
            file_chooser.Destroy()
            self.plot_graphs(paths)
            self.legend_panel.Parent.Refresh()

            self.animation_panel.Bind(wx.EVT_PAINT, self.animate_cell)
            self.animation_panel.Parent.Refresh()
            t = Thread(target=self.animate, args=(0.1,))
            t.start()
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
            paths = file_chooser.GetPaths()
            file_chooser.Destroy()

            self.model_parser = Biopepa_Model_Parser()
            self.model_parser.parse(paths[0])
            self.model_parser.build_graph()

            self.refresh_model_panel()
        else:
            file_chooser.Destroy()

    """
    Why can't I just use refresh parent like with the legend?
    TODO: see above
    """
    def refresh_model_panel(self):
        self.model_panel.Bind(wx.EVT_PAINT, self.on_paint)
        self.model_panel.Parent.Refresh()
        self.Show(False)
        self.Show(True)

    def animate_cell(self,e):
        dc2 = wx.PaintDC(self.animation_panel)
        self.cs.paint(dc2)
        self.cs2.paint(dc2)

    def animate(self, n):

        self.cs = CellSegment((10,10), 120, 0)
        self.cs2 = CellSegment((150,10), 120, 1)
        while self.world.clock < 20000:
            self.world.clock += 20000.0/600
            self.animation_panel.Refresh()
            time.sleep(n)

    """
    Get the data then plot it
    """
    def plot_graphs(self, paths):
        results = {}
        parser = BioPepaCsvParser()
        for path in paths:
            parser.parse_csv(path)
            results[path.split('/')[-1]] = parser.results_dict
        self.world.results = results
        self.world.parser = parser
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
            self.first_time = False
            self.model_parser.tree.build_tree()
            self.model_parser.tree.draw_tree_one(self.dc)
        else:
            self.model_parser.tree.draw_tree_two(self.dc)

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
            self.graph_canvas.print_figure(path, dpi=_DPI)
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
