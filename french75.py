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
import platform
from utils import open_results_file
from subprocess import call

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

        self.first_time = True
        self.cell_segments = []
        self.start_playing = False
        self.click_one = False
        self.attached_file_locations = []

        self.parse_args()

        (self.world.dispW, self.world.dispH) = self.get_resolution()

        self.splitter_left = wx.SplitterWindow(self, -1)
        self.legend_panel = wx.Panel(self.splitter_left, -1)
        splitter_right = wx.SplitterWindow(self.splitter_left, -1)
        splitter_middle = wx.SplitterWindow(splitter_right)
        splitter_right_middle = wx.SplitterWindow(splitter_right, -1)
        graph_panel = wx.Panel(splitter_middle, -1)
        self.model_panel = wx.Panel(splitter_right_middle, -1)
        self.files_panel = wx.Panel(splitter_right_middle, -1)
        self.animation_panel = wx.Panel(splitter_middle, -1)

        self.model_panel.SetBackgroundColour(_BG_COLOUR)
        self.legend_panel.SetBackgroundColour(_BG_COLOUR)
        graph_panel.SetBackgroundColour(_BG_COLOUR)
        self.animation_panel.SetBackgroundColour(_BG_COLOUR)
        self.files_panel.SetBackgroundColour(_BG_COLOUR)

        self.btn_animate_play = wx.Button(self.animation_panel, -1, 'Play')
        self.btn_animate_play.Bind(wx.EVT_BUTTON, self.play_animation)
        self.slider_time = wx.Slider(self.animation_panel, -1, value=0, minValue=0, maxValue=self.world.max_time, size=(250, -1), style=wx.SL_AUTOTICKS | wx.SL_HORIZONTAL | wx.SL_LABELS)
        self.slider_time.Bind(wx.EVT_SLIDER, self.move_animation)
        self.drop_down_species = wx.ComboBox(self.animation_panel, -1, style=wx.CB_READONLY)

        attached_files_vbox = wx.BoxSizer(wx.VERTICAL)
        attached_label = wx.StaticText(self.files_panel, -1, "Attached Files:")
        attached_files_vbox.Add(attached_label)
        self.attached_file_list = wx.ListBox(self.files_panel, -1, size=(300, 400))
        attached_files_vbox.Add(self.attached_file_list)
        attached_file_toolbar = wx.BoxSizer(wx.HORIZONTAL)
        add_files_button = wx.Button(self.files_panel, -1, "Add")
        add_files_button.Bind(wx.EVT_BUTTON, self.attach_file)
        open_files_button = wx.Button(self.files_panel, -1, "Open")
        open_files_button.Bind(wx.EVT_BUTTON, self.open_file)
        attached_file_toolbar.Add(add_files_button)
        attached_file_toolbar.Add(open_files_button)
        attached_files_vbox.Add(attached_file_toolbar, flag=wx.ALIGN_LEFT | wx.TOP)
        self.files_panel.SetSizer(attached_files_vbox)
        attached_files_vbox.Fit(self)

        animation_hbox = wx.BoxSizer(wx.HORIZONTAL)
        animation_hbox.Add(self.drop_down_species)
        animation_hbox.Add(self.btn_animate_play)
        animation_hbox.Add(self.slider_time)
        self.animation_panel.SetSizer(animation_hbox)
        animation_hbox.Fit(self)

        graph_width = int(((self.world.dispW / _COLS) * (_COLS - _NUM_OF_SIDEBARS)) / _DPI)
        graph_height = int(graph_width/_PHI)
        graph_fig = Figure((graph_width, graph_height))
        graph_fig.set_facecolor('white')

        self.graph_canvas = FigCanvas(graph_panel, -1, graph_fig)
        self.world.graph_canvas = self.graph_canvas
        self.graph_axes = graph_fig.add_subplot(111)
        graph_vbox = wx.BoxSizer(wx.VERTICAL)
        graph_vbox.Add(self.graph_canvas)

        toolbar = BioPepaToolbar(self.graph_canvas)
        (toolW, toolH) = toolbar.GetSizeTuple()
        graph_vbox.Add(toolbar)

        graph_panel.SetSizer(graph_vbox)
        graph_vbox.Fit(self)

        self.world.legend = Legend(self.legend_panel)
        self.SetMenuBar(self.build_menu_bar())

        self.splitter_left.SplitVertically(self.legend_panel, splitter_right)
        splitter_right.SplitVertically(splitter_middle, splitter_right_middle)
        splitter_middle.SplitHorizontally(graph_panel, self.animation_panel)
        splitter_right_middle.SplitHorizontally(self.model_panel, self.files_panel)

        self.Maximize()
        self.splitter_left.SetSashPosition(self.world.dispW/6)
        splitter_right.SetSashPosition(4 * self.world.dispW/6)
        splitter_middle.SetSashPosition((graph_height * _DPI) + toolH)

        #self.graph_canvas.Bind(wx.EVT_CONTEXT_MENU, self.onContext)
        self.graph_canvas.mpl_connect('button_press_event', self.onclick)

        self.SetTitle(_TITLE)
        self.Centre()
        self.Show(True)

    def open_file(self, event):
        i = self.attached_file_list.GetSelection()
        if platform.system() == "Linux":
            call(["gnome-open", self.attached_file_locations[i]])
        else:
            call(["open", self.attached_file_locations[i]])

    def attach_file(self, event):
        file_chooser = wx.FileDialog(self, message="Choose a file to attach", style=wx.OPEN | wx.CHANGE_DIR | wx.MULTIPLE)
        if file_chooser.ShowModal() == wx.ID_OK:
            paths = file_chooser.GetPaths()
            file_chooser.Destroy()
            for path in paths:
                file_name = path.split('/')[-1]
                self.attached_file_locations.append(path)
                self.attached_file_list.Append(file_name)

            self.refresh_model_panel()
        else:
            file_chooser.Destroy()

    def onclick(self, event):
        print 'button=%d, x=%d, y=%d, xdata=%f, ydata=%f' % (event.button, event.x, event.y, event.xdata, event.ydata)
        if self.world.annotation_mode == self.world._ARROW:
            if self.world.annotate and not self.click_one:
                self.click_one_x = event.xdata
                self.click_one_y = event.ydata
                self.click_one = True
                return
            if self.click_one:
                click_two_x = event.xdata
                click_two_y = event.ydata
                self.draw_plot.annotate_arrow((self.click_one_x, self.click_one_y), (click_two_x, click_two_y))
                self.click_one = False
                self.world.change_cursor(wx.CURSOR_ARROW)
                return
        elif self.world.annotation_mode == self.world._TEXT:
            if self.world.annotate:
                self.draw_plot.annotate_text((event.xdata, event.ydata), text=self.world.annotation_text)
                self.world.change_cursor(wx.CURSOR_ARROW)
                return
        elif self.world.annotation_mode == self.world._TEXT_ARROW:
            if self.world.annotate and not self.click_one:
                self.click_one_x = event.xdata
                self.click_one_y = event.ydata
                self.click_one = True
                self.world.change_cursor(wx.CURSOR_ARROW)
                return
            if self.click_one:
                self.draw_plot.annotate_arrow((self.click_one_x, self.click_one_y), (event.xdata, event.ydata), text=self.world.annotation_text)
                self.click_one = False
                self.world.change_cursor(wx.CURSOR_ARROW)
                return
        elif self.world.annotation_mode == self.world._CIRCLE:
            if self.world.annotate:
                self.draw_plot.annotate_circle((event.xdata, event.ydata))
                return

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
            (self.world.dispW, self.world.dispH) = monitor.GetGeometry().GetSize()
            (mouseX, mouseY) = wx.GetMousePosition()
            if (mouseX < self.world.dispW):
                return (self.world.dispW, self.world.dispH)

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

        self.draw_plot = Plotter(self.graph_axes, self.graph_canvas, True, self.xkcd)
        self.draw_plot.plot()
        self.splitter_left.SetSashPosition(self.splitter_left.GetSashPosition() + 1)
        self.splitter_left.SetSashPosition(self.splitter_left.GetSashPosition() - 1)
        self.legend_panel.Parent.Refresh()
        self.slider_time.SetMax(self.world.max_time)

        for species in self.world.species_dict.keys():
            for file_name in self.draw_plot.results.keys():
                for loc in self.world.species_dict[species]:
                    print self.draw_plot.results[file_name][species+"@"+loc[1]]
            self.drop_down_species.Append(species)

        self.drop_down_species.SetSelection(0)

        a = 10
        b = 40
        c = 120
        d = 0
        for file_name in self.world.results.keys():
            self.cell_segments.append(CellSegment((a, b), c, d, file_name, self.drop_down_species.GetStringSelection()))
            a += 140
            d += 1

        self.animation_panel.Bind(wx.EVT_PAINT, self.animate_cell)
        self.animation_panel.Refresh()

    """
    selects which csv files to use
    """
    def open_results_file(self, e):
        open_results_file(self)

        self.slider_time.SetMax(self.world.max_time)
        self.draw_plot = Plotter(self.graph_axes, self.graph_canvas, True, self.xkcd)
        self.draw_plot.plot()

        self.splitter_left.SetSashPosition(self.splitter_left.GetSashPosition() + 1)
        self.splitter_left.SetSashPosition(self.splitter_left.GetSashPosition() - 1)

        self.cell_segments.append(CellSegment((10, 40), 120, 0))
        self.cell_segments.append(CellSegment((150, 40), 120, 1))

        self.animation_panel.Bind(wx.EVT_PAINT, self.animate_cell)
        self.animation_panel.Refresh()

    def play_animation(self, e):
        if not self.start_playing:
            self.start_playing = True
            t4 = Thread(target=self.change_button_text, args=("Pause",))
            t = Thread(target=self.animate, args=(0.1,))
            t.start()
            t4.start()
        else:
            if self.world.clock_pause:
                self.world.clock_pause = False
                t2 = Thread(target=self.change_button_text, args=("Pause",))
                t2.start()
            else:
                self.world.clock_pause = True
                t3 = Thread(target=self.change_button_text, args=("Play",))
                t3.start()

    def change_button_text(self, title):
        print title
        self.btn_animate_play.SetLabel(title)

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
    refresh the model view pane
    """
    def refresh_model_panel(self):
        self.model_panel.Bind(wx.EVT_PAINT, self.on_paint)
        self.model_panel.Refresh()

    """
    called when the animation pane is refreshed.
    pane is refreshed by animate()
    """
    def animate_cell(self, e):
        #TODO Post in mailing list as to why this doesn't work on mac
        if (platform.system() == "Linux"):
            wx.CallAfter(self.draw_plot.vertical_line())
        dc2 = wx.PaintDC(self.animation_panel)
        for segment in self.cell_segments:
            segment.paint(dc2)

    """
    Currently called on load
    TODO: Make it be a 'play button'
    TODO: Get rid of magic numbers
    """
    def animate(self, n):
        while self.world.clock < self.world.max_time:
            while self.world.clock_pause:
                pass
            self.world.clock += self.world.clock_increment
            self.slider_time.SetValue(self.world.clock)
            self.animation_panel.Refresh()
            if (platform.system() != "Linux"):
                self.draw_plot.vertical_line()
            time.sleep(n)

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
            self.draw_plot.redraw_legend = False
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

    def move_animation(self, e):
        self.world.clock = self.slider_time.GetValue()
        for segment in self.cell_segments:
            segment.update_clock()

if __name__ == '__main__':
    app = wx.App()
    gui = French75(None)
    gui.Show()
    app.MainLoop()
