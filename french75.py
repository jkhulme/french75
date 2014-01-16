from biopepa_model_parser import Biopepa_Model_Parser
from plotter import Plotter
import wx
import matplotlib
matplotlib.use('WXAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigCanvas
from legend import Legend
import os
from custom_ui_elements import BioPepaToolbar
from session_creator import SessionWizard
from worldstate import WorldState
from cell_segment import CellSegment
import time
from threading import Thread
import platform
from utils import euclid_distance, point_to_line_distance, calc_graph_size, reset_sash_position, refresh_plot
from subprocess import call
from annotation import Annotation
import wx.lib.scrolledpanel as scrolled

_DPI = 80
_BG_COLOUR = 'white'
_TITLE = 'French75'
_PHI = 1.618
_LEFT_BUTTON = 1
_RIGHT_BUTTON = 3
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
    self.world.draw_plot - the plotter which we use to draw lines
    """

    def __init__(self, *args, **kwargs):
        """
        Sets up the UI, binds the events etc
        """
        super(French75, self).__init__(*args, **kwargs)
        self.Maximize()
        self.panels = []
        self.panel_vboxes = []
        self.world = WorldState.Instance()
        (self.world.session_dict['dispW'], self.world.session_dict['dispH']) = self.GetSize()
        self.end_of_time = False
        self.i = 0
        #self.save = False

        self.splitter_left = wx.SplitterWindow(self, -1)
        self.legend_panel = scrolled.ScrolledPanel(self.splitter_left, -1)
        splitter_right = wx.SplitterWindow(self.splitter_left, -1)
        splitter_middle = wx.SplitterWindow(splitter_right)
        splitter_right_middle = wx.SplitterWindow(splitter_right, -1)
        self.graph_panel = wx.Panel(splitter_middle, -1)
        self.model_panel = wx.Panel(splitter_right_middle, -1)
        self.files_panel = wx.Panel(splitter_right_middle, -1)
        #self.animation_panel = wx.Panel(splitter_middle, -1)
        self.animation_panel = scrolled.ScrolledPanel(splitter_middle, -1)

        self.model_panel.SetBackgroundColour(_BG_COLOUR)
        self.legend_panel.SetBackgroundColour(_BG_COLOUR)
        self.graph_panel.SetBackgroundColour(_BG_COLOUR)
        self.animation_panel.SetBackgroundColour(_BG_COLOUR)
        self.files_panel.SetBackgroundColour(_BG_COLOUR)

        self.btn_animate_play = wx.Button(self.animation_panel, -1, 'Play')
        self.btn_animate_play.Bind(wx.EVT_BUTTON, self.play_animation)

        self.slider_time = wx.Slider(self.animation_panel, -1, value=0, minValue=0, maxValue=self.world.session_dict['max_time'], size=(250, -1), style=wx.SL_AUTOTICKS | wx.SL_HORIZONTAL | wx.SL_LABELS)
        self.slider_time.Bind(wx.EVT_SLIDER, self.move_animation)

        self.drop_down_species = wx.ComboBox(self.animation_panel, -1, style=wx.CB_READONLY)
        self.drop_down_species.Bind(wx.wx.EVT_COMBOBOX, self.change_animation_species)
        self.switch_animation_button = wx.Button(self.animation_panel, -1, "<->")
        self.switch_animation_button.Bind(wx.EVT_BUTTON, self.switch_animation)
        self.drop_down_files = wx.ComboBox(self.animation_panel, -1, style=wx.CB_READONLY)

        attached_files_vbox = wx.BoxSizer(wx.VERTICAL)
        attached_label = wx.StaticText(self.files_panel, -1, "Attached Files:")
        attached_files_vbox.Add(attached_label)
        self.attached_file_list = wx.ListBox(self.files_panel, -1, size=(300, 400))
        attached_files_vbox.Add(self.attached_file_list)
        attached_file_toolbar = wx.BoxSizer(wx.HORIZONTAL)
        self.add_files_button = wx.Button(self.files_panel, -1, "Add")
        self.add_files_button.Bind(wx.EVT_BUTTON, self.attach_file)

        self.open_files_button = wx.Button(self.files_panel, -1, "Open")
        self.open_files_button.Bind(wx.EVT_BUTTON, self.open_file)

        attached_file_toolbar.Add(self.add_files_button)
        attached_file_toolbar.Add(self.open_files_button)
        attached_files_vbox.Add(attached_file_toolbar, flag=wx.ALIGN_LEFT | wx.TOP)
        self.files_panel.SetSizer(attached_files_vbox)
        attached_files_vbox.Fit(self)

        animation_vbox = wx.BoxSizer(wx.VERTICAL)
        animation_hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.animation_panels_hbox = wx.BoxSizer(wx.HORIZONTAL)
        animation_hbox.Add(self.drop_down_files)
        animation_hbox.Add(self.switch_animation_button)
        animation_hbox.Add(self.drop_down_species)
        animation_hbox.Add(self.btn_animate_play)
        animation_hbox.Add(self.slider_time)
        animation_vbox.Add(animation_hbox)
        animation_vbox.Add(self.animation_panels_hbox)
        self.animation_panel.SetSizer(animation_vbox)
        animation_vbox.Fit(self)
        animation_hbox.Fit(self)
        self.animation_panel.SetupScrolling(scroll_y=False)

        (graph_width, graph_height) = calc_graph_size(_DPI, _COLS, _NUM_OF_SIDEBARS, _PHI)
        self.world.session_dict['graph_width'] = graph_width
        self.world.session_dict['graph_height'] = graph_height
        graph_fig = Figure((graph_width, graph_height))
        graph_fig.set_facecolor('white')

        self.graph_canvas = FigCanvas(self.graph_panel, -1, graph_fig)
        self.world.graph_canvas = self.graph_canvas
        self.graph_axes = graph_fig.add_subplot(111)
        self.world.graph_axes = self.graph_axes
        graph_vbox = wx.BoxSizer(wx.VERTICAL)
        graph_vbox.Add(self.graph_canvas)

        self.toolbar = BioPepaToolbar(self.graph_canvas)
        (toolW, toolH) = self.toolbar.GetSizeTuple()
        graph_vbox.Add(self.toolbar)

        self.graph_panel.SetSizer(graph_vbox)
        graph_vbox.Fit(self)

        self.world.legend = Legend(self.legend_panel)
        self.SetMenuBar(self.build_menu_bar())

        self.splitter_left.SplitVertically(self.legend_panel, splitter_right)
        splitter_right.SplitVertically(splitter_middle, splitter_right_middle)
        splitter_middle.SplitHorizontally(self.graph_panel, self.animation_panel)
        splitter_right_middle.SplitHorizontally(self.model_panel, self.files_panel)

        #self.Maximize()
        self.splitter_left.SetSashPosition(self.world.session_dict['dispW']/6)
        splitter_right.SetSashPosition(4 * self.world.session_dict['dispW']/6)
        splitter_middle.SetSashPosition((graph_height * _DPI) + toolH)

        #self.graph_canvas.Bind(wx.EVT_CONTEXT_MENU, self.onContext)
        self.graph_canvas.mpl_connect('button_press_event', self.onclick)
        self.graph_canvas.mpl_connect('motion_notify_event', self.move_mouse)

        self.SetTitle(_TITLE)
        self.world.update_title = self.SetTitle
        self.world.get_title = self.GetTitle
        self.enable_all(False)
        self.filem_new_session.Enable(True)
        self.filem_load_session.Enable(True)
        self.Maximize()

    def enable_all(self, state):
        """
        Want stuff disables until after session has been set up
        """
        self.toolbar.enable_all(state)
        self.filem_new_session.Enable(state)
        self.filem_save_session.Enable(state)
        self.filem_load_session.Enable(state)
        self.filem_open_results_save_plot.Enable(state)
        #self.filem_open_results_open_model.Enable(state)
        #self.filem_open_results_save_model.Enable(state)
        self.annotationm_toggle.Enable(state)
        #Test on DICE, see if XKCD mode can work
        #self.xkcdm_toggle.Enable(state)
        self.undo_m.Enable(state)
        self.redo_m.Enable(state)

        if self.world.session_dict['tree_list'] and state:
            self.btn_animate_play.Enable(state)
            self.slider_time.Enable(state)
            self.drop_down_species.Enable(state)

        self.add_files_button.Enable(state)
        self.open_files_button.Enable(state)

    def move_mouse(self, event):
        """
        Handles the drawing of the arrow when deciding where to annotate
        """
        if self.world.draw_plot:
            if self.world.session_dict['click_one']:
                self.world.session_dict['temp_annotation'] = Annotation(self.world._ARROW, (self.world.session_dict['click_one_x'], self.world.session_dict['click_one_y']), (event.xdata, event.ydata))
            #TODO: Don't replot mid animation
            if self.world.session_dict['annotate']:
                self.world.session_dict['redraw_legend'] = False
                self.world.draw_plot.plot()
                self.world.session_dict['redraw_legend'] = True

    def open_file(self, event):
        """
        Opening attached files, must be a better way of doing this
        """
        i = self.attached_file_list.GetSelection()
        if platform.system() == "Linux":
            call(["gnome-open", self.world.session_dict['attached_file_locations'][i]])
        else:
            call(["open", self.world.session_dict['attached_file_locations'][i]])

    def attach_file(self, event):
        file_chooser = wx.FileDialog(self, message="Choose a file to attach", style=wx.OPEN | wx.CHANGE_DIR | wx.MULTIPLE)
        if file_chooser.ShowModal() == wx.ID_OK:
            paths = file_chooser.GetPaths()
            file_chooser.Destroy()
            for path in paths:
                file_name = path.split('/')[-1]
                self.world.session_dict['attached_file_locations'].append(path)
                self.attached_file_list.Append(file_name)

            self.refresh_model_panel()
        else:
            file_chooser.Destroy()

    def onclick(self, event):
        """
        On the graph canvas
        """
        if self.world.draw_plot:
            if event.button == _LEFT_BUTTON:
                self.left_click_handler(event)
            elif event.button == _RIGHT_BUTTON:
                self.right_click_handler(event)

    def left_click_handler(self, event):
        """
        Currently checks which annotation you want to draw and then creates it
        """
        if self.world.session_dict['annotation_mode'] == self.world._ARROW:
            if self.world.session_dict['annotate'] and not self.world.session_dict['click_one']:
                self.world.session_dict['click_one_x'] = event.xdata
                self.world.session_dict['click_one_y'] = event.ydata
                self.world.session_dict['click_one'] = True
                return
            if self.world.session_dict['click_one']:
                click_two_x = event.xdata
                click_two_y = event.ydata
                self.world.draw_plot.annotate_arrow((self.world.session_dict['click_one_x'], self.world.session_dict['click_one_y']), (click_two_x, click_two_y), colour='black')
                self.world.session_dict['click_one'] = False
                self.world.change_cursor(wx.CURSOR_ARROW)
                self.world.annotation_mode = self.world._NONE
                self.world.session_dict['temp_annotation'] = None
                self.world.session_dict['redraw_legend'] = False
                self.world.draw_plot.plot()
                self.world.session_dict['redraw_legend'] = True
                self.world.push_state()
                return
            elif self.world.session_dict['annotation_mode'] == self.world._TEXT:
                if self.world.session_dict['annotate']:
                    self.world.draw_plot.annotate_text((event.xdata, event.ydata), text=self.world.session_dict['annotation_text'])
                    self.world.change_cursor(wx.CURSOR_ARROW)
                    self.world.session_dict['annotation_mode'] = self.world._NONE
                    self.world.push_state()
                    return
            elif self.world.session_dict['annotation_mode'] == self.world._TEXT_ARROW:
                if self.world.session_dict['annotate'] and not self.world.session_dict['click_one']:
                    self.world.session_dict['click_one_x'] = event.xdata
                    self.world.session_dict['click_one_y'] = event.ydata
                    self.world.session_dict['click_one'] = True
                    self.world.change_cursor(wx.CURSOR_ARROW)
                    return
                if self.world.session_dict['click_one']:
                    self.world.draw_plot.annotate_arrow((self.world.session_dict['click_one_x'], self.world.session_dict['click_one_y']), (event.xdata, event.ydata), text=self.world.session_dict['annotation_text'], colour='black')
                    self.world.session_dict['click_one'] = False
                    self.world.change_cursor(wx.CURSOR_ARROW)
                    self.world.session_dict['annotation_mode'] = self.world._NONE
                    self.world.session_dict['temp_annotation'] = None
                    self.world.session_dict['redraw_legend'] = False
                    self.world.draw_plot.plot()
                    self.world.session_dict['redraw_legend'] = True
                    self.world.push_state()
                    return
            elif self.world.session_dict['annotation_mode'] == self.world._CIRCLE:
                if self.world.session_dict['annotate']:
                    self.world.draw_plot.annotate_circle((event.xdata, event.ydata), colour='black')
                    self.world.session_dict['annotation_mode'] = self.world._NONE
                    self.world.push_state()
                    return

    def right_click_handler(self, event):
        """
        Select existing annotations, offer to edit or delete
        """
        self.selected_annotation = None
        for annotation in self.world.session_dict['annotations']:
            dist = point_to_line_distance((annotation.x1/float(self.world.session_dict['max_time']), annotation.y1/float(self.world.session_dict['max_height'])),
                                          (annotation.x2/float(self.world.session_dict['max_time']), annotation.y2/float(self.world.session_dict['max_height'])),
                                          (event.xdata/float(self.world.session_dict['max_time']), event.ydata/float(self.world.session_dict['max_height'])))
            if dist < 0.025:
                if self.selected_annotation is None:
                    self.selected_annotation = annotation
                elif euclid_distance((event.xdata, event.ydata), (self.selected_annotation.x1, self.selected_annotation.ys)):
                    self.selected_annotation = annotation
        if self.selected_annotation is not None:
            self.selected_annotation.colour = 'red'
            refresh_plot()
            self.annotation_menu()
            self.selected_annotation.colour = 'black'
            refresh_plot()
        else:
            print "Missed annotation"

    def annotation_menu(self):
        annotate_menu = wx.Menu()
        m_edit_annotation = annotate_menu.Append(wx.ID_ANY, 'Edit')
        m_delete_annotation = annotate_menu.Append(wx.ID_ANY, 'Delete')
        #self.m_toggle_annotation = annotate_menu.AppendCheckItem(wx.ID_ANY, '&Show')
        #self.m_toggle_annotation.Check(True)
        self.Bind(wx.EVT_MENU, self.edit_annotation_text, m_edit_annotation)
        self.Bind(wx.EVT_MENU, self.delete_annotation, m_delete_annotation)
        #self.Bind(wx.EVT_MENU, self.show_hide_annotation, self.m_toggle_annotation)
        self.graph_panel.PopupMenu(annotate_menu)
        annotate_menu.Destroy()

    """
    def show_hide_annotation(self, e):
        is_checked = self.m_toggle_annotation.IsChecked()
        new_check = not is_checked
        print new_check
        self.m_toggle_annotation.Check(check=False)
        print self.m_toggle_annotation.IsChecked()
        self.selected_annotation.show = self.m_toggle_annotation.IsChecked()
    """

    def edit_annotation_text(self, event):
        self.get_label()
        if self.world.session_dict['annotation_text'] != "":
            self.selected_annotation.text = self.world.session_dict['annotation_text']
            if self.selected_annotation.type == self.world._ARROW:
                self.selected_annotation.type = self.world._TEXT_ARROW
        self.world.push_state()

    def delete_annotation(self, event):
        new_annotation_list = [annotation for annotation in self.world.session_dict['annotations'] if annotation != self.selected_annotation]
        self.world.session_dict['annotations'] = new_annotation_list
        self.world.push_state()

    def get_label(self):
         dialog = wx.TextEntryDialog(None, "What kind of text would you like to enter?","Text Entry", "Default Value", style=wx.OK|wx.CANCEL)
         self.txtctrl = dialog.FindWindowById(3000)
         #Not the right thing
         #self.txtctrl.Bind(wx.EVT_LEFT_DOWN, self.clear_text_box)
         if dialog.ShowModal() == wx.ID_OK:
             self.world.session_dict['annotation_text'] = dialog.GetValue()

    """
    because of cases where there are multiple monitors we need to go through
    all the monitors and decide which one to use - base this on mouse position.
    n/b - self.GetSize() might need to be used

    def get_resolution(self):
        for monitor in [wx.Display(i) for i in range(wx.Display.GetCount())]:
            (self.world.session_dict['dispW'], self.world.session_dict['dispH']) = monitor.GetGeometry().GetSize()
            (mouseX, mouseY) = wx.GetMousePosition()
            if (mouseX < self.world.session_dict['dispW']):
                return (self.world.session_dict['dispW'], self.world.session_dict['dispH'])
    Currently not called
    """

    """
    The menu bar.
    Again could take this out to be its own class
    Need to organise the menu a bit better - look at mac style guidelines
    """
    def build_menu_bar(self):
        menubar = wx.MenuBar()
        menubar.SetBackgroundColour(_BG_COLOUR)

        file_menu = wx.Menu()
        self.filem_new_session = file_menu.Append(wx.ID_NEW, '&New Session')
        self.filem_save_session = file_menu.Append(wx.ID_ANY, '&Save Session')
        self.filem_load_session  = file_menu.Append(wx.ID_ANY, '&Load Session')
        file_menu.AppendSeparator()
        self.filem_open_results_save_plot = file_menu.Append(wx.ID_SAVE, 'Export Graph')
        #self.filem_export_animation = file_menu.Append(wx.ID_ANY, 'Export Animation')

        #file_menu.AppendSeparator()
        #self.filem_open_results_open_model = file_menu.Append(wx.ID_ANY, '&View Model')

        #self.filem_open_results_save_model = file_menu.Append(wx.ID_ANY, 'Save &Model')


        menubar.Append(file_menu, '&File')

        self.Bind(wx.EVT_MENU, self.new_session, self.filem_new_session)
        self.Bind(wx.EVT_MENU, self.save_session, self.filem_save_session)
        self.Bind(wx.EVT_MENU, self.load_session, self.filem_load_session)
        #self.Bind(wx.EVT_MENU, self.open_model_file, self.filem_open_results_open_model)
        #self.Bind(wx.EVT_MENU, self.save_snapshot, self.filem_open_results_save_model)
        self.Bind(wx.EVT_MENU, self.on_save_plot, self.filem_open_results_save_plot)
        #self.Bind(wx.EVT_MENU, self.export_animation, self.filem_export_animation)

        preferences_menu = wx.Menu()
        self.annotationm_toggle = preferences_menu.AppendCheckItem(wx.ID_ANY, '&Annotations')
        self.annotationm_toggle.Check()
        #self.xkcdm_toggle = preferences_menu.AppendCheckItem(wx.ID_ANY, '&xkcd mode')

        menubar.Append(preferences_menu, '&Preferences')

        self.Bind(wx.EVT_MENU, self.toggle_annotations, self.annotationm_toggle)
        #self.Bind(wx.EVT_MENU, self.toggle_xkcd, self.xkcdm_toggle)

        edit_menu = wx.Menu()
        self.undo_m = edit_menu.Append(wx.ID_ANY, '&Undo')

        self.redo_m = edit_menu.Append(wx.ID_ANY, '&Redo')

        menubar.Append(edit_menu, '&Edit')
        self.Bind(wx.EVT_MENU, self.undo, self.undo_m)
        self.Bind(wx.EVT_MENU, self.redo, self.redo_m)

        return menubar

    def undo(self, event):
        self.world.undo()
        refresh_plot()

    def redo(self, event):
        pass

    def toggle_xkcd(self, event):
        self.toggle_param('xkcd')
        matplotlib.pyplot.xkcd()

    def toggle_annotations(self, event):
        self.toggle_param('draw_annotations')

    def toggle_param(self, param):
        self.world.session_dict[param] = not self.world.session_dict[param]
        refresh_plot()


    """
    Session starter dialogue
    """
    def new_session(self, e):
        self.world.temp_session_dict = self.world.session_dict
        session_dialog = SessionWizard(title='Session Starter')
        session_dialog.run()
        session_dialog.Destroy()

        if session_dialog.state == session_dialog._FINISHED:
            self.world.temp_session_dict = None
            self.world.session_dict['title'] = session_dialog.title_text.GetLineText(0)
            session_dialog.parse_species()
            self.sessiony_stuff()

        else:
            self.world.session_dict = self.world.temp_session_dict
            self.world.temp_session_dict = None

    def sessiony_stuff(self):
        self.world.draw_plot = Plotter(self.graph_axes)
        self.world.draw_plot.plot()
        reset_sash_position(self.splitter_left)
        self.legend_panel.Parent.Refresh()
        self.slider_time.SetMax(self.world.session_dict['max_time'])

        if self.world.session_dict['tree_list']:
            for species in self.list_of_species():
                self.drop_down_species.Append(species)
            for file_name in self.world.session_dict['results'].keys():
                self.drop_down_files.Append(file_name)
            self.drop_down_species.SetSelection(0)
            self.drop_down_files.SetSelection(0)

            self.create_cell_segments_by_file()


        self.world.push_state()
        self.enable_all(True)

    def change_animation_species(self, e):
        self.create_cell_segments()

    def create_cell_segments_by_file(self):
        (a_width, a_height) = self.animation_panel.GetSize()
        for child in self.animation_panel.GetChildren():
            try:
                int(child.GetName())
                child.Destroy()
            except:
                pass
        self.panels = []
        self.panel_vboxes = []
        self.world.cell_segments = []
        #TODO: Fix these magic numbers
        a = 10
        b = (a_height * 0.7) - 10
        c = (a_height * 0.7) - 20
        d = 0
        for i, file_name in enumerate(self.world.session_dict['results'].keys()):
            small_vbox = wx.BoxSizer(wx.VERTICAL)
            self.panel_vboxes.append(small_vbox)
            title = wx.StaticText(self.animation_panel, -1, file_name, name=str(i))
            small_vbox.Add(title,0,wx.EXPAND|wx.ALL,border=2)
            panel = wx.Panel(self.animation_panel, -1,size=(a_height*0.7,a_height*0.7), name=str(i))
            small_vbox.Add(panel,0,wx.EXPAND|wx.ALL,border=2)
            panel.SetBackgroundColour('white')
            panel.Bind(wx.EVT_PAINT, self.animate_cell)
            self.panels.append(panel)
            self.animation_panels_hbox.Add(small_vbox,0,wx.EXPAND|wx.ALL,border=2)
            self.world.cell_segments.append(CellSegment((a, b), c, d, file_name, self.drop_down_species.GetStringSelection()))
        self.animation_panel.Layout()
        self.animation_panel.SetupScrolling(scroll_y=False)
        for panel in self.panels:
            panel.Refresh()

    def create_cell_segments_by_species(self):
        (a_width, a_height) = self.animation_panel.GetSize()
        for child in self.animation_panel.GetChildren():
            try:
                int(child.GetName())
                child.Destroy()
            except:
                pass
        self.panels = []
        self.panel_vboxes = []
        self.world.cell_segments = []
        #TODO: Fix these magic numbers
        a = 10
        b = (a_height * 0.7) - 10
        c = (a_height * 0.7) - 20
        d = 0
        for i, species_name in enumerate(self.list_of_species()):
            if species_name != "Time":
                small_vbox = wx.BoxSizer(wx.VERTICAL)
                self.panel_vboxes.append(small_vbox)
                title = wx.StaticText(self.animation_panel, -1, species_name, name=str(i))
                small_vbox.Add(title,0,wx.EXPAND|wx.ALL,border=2)
                panel = wx.Panel(self.animation_panel, -1,size=(a_height*0.7,a_height*0.7), name=str(i))
                small_vbox.Add(panel,0,wx.EXPAND|wx.ALL,border=2)
                panel.SetBackgroundColour('white')
                panel.Bind(wx.EVT_PAINT, self.animate_cell)
                self.panels.append(panel)
                self.animation_panels_hbox.Add(small_vbox,0,wx.EXPAND|wx.ALL,border=2)
                self.world.cell_segments.append(CellSegment((a, b), c, d, self.drop_down_files.GetStringSelection(), species_name.split("@")[0]))
        self.animation_panel.Layout()
        self.animation_panel.SetupScrolling(scroll_y=False)
        for panel in self.panels:
            panel.Refresh()

    def switch_animation(self, e):
        if self.drop_down_species.IsEnabled():
            self.drop_down_species.Enable(False)
            self.drop_down_files.Enable(True)
            self.create_cell_segments_by_species()
        else:
            self.drop_down_species.Enable(True)
            self.drop_down_files.Enable(False)
            self.create_cell_segments_by_file()

    def list_of_species(self):
        species_list = []
        for key, item in self.world.session_dict['species_dict'].items():
            for species in item:
                if species not in species_list:
                    species_list.append(species)
        return species_list

    def save_session(self, e):
        """
        Serialize the data with pickling and write it to a file.
        Uses the .f75 extension
        """
        file_choices = "F75 (*.f75)|*.f75"

        dlg = wx.FileDialog(
            self,
            message="Save session as...",
            defaultDir=os.getcwd(),
            defaultFile="my_session.f75",
            wildcard=file_choices,
            style=wx.SAVE)

        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            with open(path, 'wb') as f:
                f.write(self.world.pickle_session())
            self.SetTitle(_TITLE)
        else:
            dlg.Destroy()


    def load_session(self, e):
        file_chooser = wx.FileDialog(
            self,
            message="Choose a file",
            wildcard="*.f75",
            style=wx.OPEN | wx.CHANGE_DIR)
        if file_chooser.ShowModal() == wx.ID_OK:
            path = file_chooser.GetPath()
            with open(path, 'r') as f:
                data = f.readlines()
            self.world.unpickle_session(''.join(data))
            self.sessiony_stuff()
            self.SetTitle(_TITLE)
        else:
            file_chooser.Destroy()

    def play_animation(self, e):
        """
        Create new threads, change button text
        """
        if not self.world.session_dict['start_playing']:
            self.world.session_dict['clock'] = 0
            self.slider_time.SetValue(0)
            for line_dict in self.world.session_dict['lines'].values():
                for line in line_dict.values():
                    line.counter = 0
            self.world.session_dict['clock_pause'] = False
            self.world.session_dict['start_playing'] = True
            t4 = Thread(target=self.change_button_text, args=("Pause",))
            t = Thread(target=self.animate, args=(0.1,))
            t.start()
            t4.start()
        else:
            if self.world.session_dict['clock_pause']:
                self.world.session_dict['clock_pause'] = False
                t2 = Thread(target=self.change_button_text, args=("Pause",))
                t2.start()
            else:
                self.world.session_dict['clock_pause'] = True
                t3 = Thread(target=self.change_button_text, args=("Play",))
                t3.start()

    def change_button_text(self, title):
        self.btn_animate_play.SetLabel(title)

    """
    Which biopepa model to display

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

    """
    refresh the model view pane

    def refresh_model_panel(self):
        self.model_panel.Bind(wx.EVT_PAINT, self.on_paint)
        self.model_panel.Refresh()
    """

    """
    called when the animation pane is refreshed. -- OnPaint
    pane is refreshed by animate()
    update the position of the vertical line.  Draw each of the cell segments
    """
    def animate_cell(self, e):
        wx.CallAfter(self.world.draw_plot.vertical_line)
        panel = e.GetEventObject()
        idx = int(panel.GetName())
        dc2 = wx.PaintDC(panel)
        self.world.cell_segments[idx].paint(dc2)
        self.i += 1
        #if self.save:
        #    self.save_snapshot(dc2, self.i)

    """
    Run by the thread
    Check the time and whether we are paused or not, if not then update the
    clock and redraw
    """
    def animate(self, n):
        while self.world.session_dict['clock'] < self.world.session_dict['max_time']:
            while self.world.session_dict['clock_pause']:
                pass
            time.sleep(n)
            self.world.session_dict['clock'] += self.world.session_dict['clock_increment']
            self.slider_time.SetValue(self.world.session_dict['clock'])
            for panel in self.panels:
                panel.Refresh()

        self.slider_time.SetValue(self.world.session_dict['max_time'])
        self.change_button_text('Play')
        self.world.session_dict['start_playing'] = False

    """
    Handles drawing of the model
    """
    def on_paint(self, e):
        self.dc = wx.PaintDC(self.model_panel)
        if self.world.session_dict['first_time']:
            self.world.session_dict['first_time'] = False
            #Do this when parsing the model?  Then I can remove this IF
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
            self.world.draw_plot.mpl_legend = True
            self.world.session_dict['redraw_legend'] = False
            self.world.draw_plot.plot()
            self.graph_canvas.print_figure(path, dpi=_DPI)
            self.world.draw_plot.mpl_legend = False
            self.world.draw_plot.plot()

    """
    Save a picture of the model
    based largely on code posted to wxpython-users by Andrea Gavana 2006-11-08

    def save_snapshot(self, dc, i):
        dcSource = dc
        size = dcSource.Size
        bmp = wx.EmptyBitmap(200, 200)
        memDC = wx.MemoryDC()
        memDC.SelectObject(bmp)
        memDC.Blit(0, 0, size.width, size.height, dcSource, 0, 0)
        memDC.SelectObject(wx.NullBitmap)
        img = bmp.ConvertToImage()
        img.SaveFile(str(i) + '.png', wx.BITMAP_TYPE_PNG)
    """

    def move_animation(self, e):
        """
        Bound to the slider when you move it -- updates the session clock
        """
        self.world.session_dict['clock'] = self.slider_time.GetValue()
        for segment in self.world.cell_segments:
            segment.update_clock()

    def export_animation(self, e):
        self.save = True
        self.play_animation(None)

if __name__ == '__main__':
    app = wx.App()
    gui = French75(None)
    gui.Show()
    app.MainLoop()
    app.Destroy()
