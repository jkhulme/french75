import wx
import matplotlib
matplotlib.use('WXAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigCanvas
from legend import Legend
import os
from plotter import Plotter
from custom_ui_elements import BioPepaToolbar
from session_creator import SessionWizard
from worldstate import WorldState
from cell_segment import CellSegment
import time
from threading import Thread
import platform
from utils import euclid_distance, point_to_line_distance, calc_graph_size, refresh_plot
from subprocess import call
from annotation import Annotation
import wx.lib.scrolledpanel as scrolled
from annotation_dialogue import AnnotationDialogue
from rpc_server import French75Server
from rpc_client import French75Client

_DPI = 80
_BG_COLOUR = 'white'
_TITLE = 'French75'
_PHI = 1.618
_LEFT_BUTTON = 1
_RIGHT_BUTTON = 3
_COLS = 6
_NUM_OF_SIDEBARS = 2


class French75(wx.Frame):

    def __init__(self, *args, **kwargs):
        """
        Sets up the UI, binds the events etc
        """
        super(French75, self).__init__(*args, **kwargs)
        self.world = WorldState.Instance()
        self.Maximize()
        (self.world.dispW, self.world.dispH) = self.GetSize()

        splitter_far_right = wx.SplitterWindow(self, -1)
        splitter_horiz_middle = wx.SplitterWindow(splitter_far_right, -1)
        splitter_vert_middle = wx.SplitterWindow(splitter_horiz_middle)
        splitter_far_right_middle = wx.SplitterWindow(splitter_far_right, -1)

        self.legend_panel = scrolled.ScrolledPanel(splitter_vert_middle, -1)
        self.graph_panel = wx.Panel(splitter_vert_middle, -1)

        self.legend_panel.SetBackgroundColour(_BG_COLOUR)
        self.graph_panel.SetBackgroundColour(_BG_COLOUR)

        """
        Animation Panel Setup
        """
        self.animation_panel = scrolled.ScrolledPanel(splitter_horiz_middle, -1)
        self.animation_panel.SetBackgroundColour(_BG_COLOUR)

        self.btn_animate_play = wx.Button(self.animation_panel, -1, 'Play')
        self.btn_animate_play.Bind(wx.EVT_BUTTON, self.play_animation)

        self.slider_time = wx.Slider(self.animation_panel, -1, value=0, minValue=0, maxValue=self.world.session_dict['max_time'], style=wx.SL_AUTOTICKS | wx.SL_HORIZONTAL | wx.SL_LABELS)
        self.slider_time.Bind(wx.EVT_SLIDER, self.move_animation)
        self.slider_time.Bind(wx.EVT_SCROLL_THUMBRELEASE, self.released_slider)

        self.drop_down_species = wx.ComboBox(self.animation_panel, -1, style=wx.CB_READONLY)
        self.drop_down_species.Bind(wx.wx.EVT_COMBOBOX, self.change_animation_species)

        self.switch_animation_button = wx.Button(self.animation_panel, -1, "<->")
        self.switch_animation_button.Bind(wx.EVT_BUTTON, self.switch_animation)

        self.drop_down_files = wx.ComboBox(self.animation_panel, -1, style=wx.CB_READONLY)
        self.drop_down_files.Bind(wx.wx.EVT_COMBOBOX, self.change_animation_file)

        line1 = wx.StaticLine(self.animation_panel, -1, style=wx.LI_VERTICAL)
        line3 = wx.StaticLine(self.animation_panel, -1, style=wx.LI_VERTICAL)
        line2 = wx.StaticLine(self.animation_panel)

        animation_vbox = wx.BoxSizer(wx.VERTICAL)
        animation_hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.animation_panels_hbox = wx.BoxSizer(wx.HORIZONTAL)

        animation_hbox.Add(self.drop_down_files, 0, wx.ALL, 10)
        animation_hbox.Add(self.switch_animation_button, 0, wx.TOP, 12)
        animation_hbox.Add(self.drop_down_species, 0, wx.ALL, 10)
        animation_hbox.Add(line1, 0, wx.EXPAND|wx.ALL, 5)
        animation_hbox.Add(self.btn_animate_play, 0, wx.TOP, 12)
        animation_hbox.Add(line3, 0, wx.EXPAND|wx.ALL, 5)
        animation_hbox.Add(self.slider_time, 0, wx.BOTTOM|wx.EXPAND|wx.ALIGN_RIGHT, 5)

        animation_vbox.Add(animation_hbox, 0)
        animation_vbox.Add(line2, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 10)
        animation_vbox.Add(self.animation_panels_hbox)

        self.animation_panel.SetSizer(animation_vbox)
        self.animation_panel.Layout()
        self.animation_panel.SetupScrolling(scroll_y=False)

        """
        Attached Files Panel Setup
        """
        attachment_panel = wx.Panel(splitter_far_right_middle, -1)
        attachment_panel.SetBackgroundColour(_BG_COLOUR)

        attached_files_vbox = wx.BoxSizer(wx.VERTICAL)
        attached_file_toolbar = wx.BoxSizer(wx.HORIZONTAL)

        attached_label = wx.StaticText(attachment_panel, -1, "Attached Files:")
        attached_files_vbox.Add(attached_label, 0, wx.EXPAND|wx.TOP|wx.LEFT, 5)

        self.attached_file_list = wx.ListBox(attachment_panel, -1, size=(300, 300))
        attached_files_vbox.Add(self.attached_file_list)

        self.add_files_button = wx.Button(attachment_panel, -1, "Add")
        self.add_files_button.Bind(wx.EVT_BUTTON, self.attach_file)

        self.open_files_button = wx.Button(attachment_panel, -1, "Open")
        self.open_files_button.Bind(wx.EVT_BUTTON, self.open_attached_file)

        attached_file_toolbar.Add(self.add_files_button, 0, wx.ALL, 5)
        attached_file_toolbar.Add(self.open_files_button, 0, wx.ALL, 5)

        attached_files_vbox.Add(attached_file_toolbar, 0, wx.ALL|wx.ALIGN_CENTRE, 5)

        attachment_panel.SetSizer(attached_files_vbox)
        attached_files_vbox.Fit(self)

        """
        Animation Annotations Panel Setup
        """

        annotation_panel = wx.Panel(splitter_far_right_middle, -1)
        annotation_panel.SetBackgroundColour(_BG_COLOUR)

        anime_annotations_vbox = wx.BoxSizer(wx.VERTICAL)
        anime_annotations_toolbar = wx.BoxSizer(wx.HORIZONTAL)

        anime_annotations_label = wx.StaticText(annotation_panel, -1, "Animation Annotations:")
        anime_annotations_vbox.Add(anime_annotations_label, 0, wx.EXPAND|wx.TOP|wx.LEFT, 5)

        self.anime_annotations_list = wx.ListBox(annotation_panel, -1, size=(300, 300))
        anime_annotations_vbox.Add(self.anime_annotations_list)

        self.add_anime_annotation_button = wx.Button(annotation_panel, -1, "Add")
        self.add_anime_annotation_button.Bind(wx.EVT_BUTTON, self.add_anime_annotation)

        self.delete_anime_annotation_button = wx.Button(annotation_panel, -1, "Delete")
        self.delete_anime_annotation_button.Bind(wx.EVT_BUTTON, self.remove_anime_annotation)

        anime_annotations_toolbar.Add(self.add_anime_annotation_button, 0, wx.ALL, 5)
        anime_annotations_toolbar.Add(self.delete_anime_annotation_button, 0, wx.ALL, 5)

        anime_annotations_vbox.Add(anime_annotations_toolbar, 0, wx.ALL|wx.ALIGN_CENTRE, 5)

        annotation_panel.SetSizer(anime_annotations_vbox)
        anime_annotations_vbox.Fit(self)

        """
        Graph Panel Setup
        """

        (graph_width, graph_height) = calc_graph_size(_DPI, _COLS, _NUM_OF_SIDEBARS, _PHI)

        graph_fig = Figure((graph_width, graph_height))
        graph_fig.set_facecolor('white')

        self.graph_canvas = FigCanvas(self.graph_panel, -1, graph_fig)
        self.graph_axes = graph_fig.add_subplot(111)

        graph_vbox = wx.BoxSizer(wx.VERTICAL)
        graph_vbox.Add(self.graph_canvas)

        self.toolbar = BioPepaToolbar(self.graph_canvas)
        (toolW, toolH) = self.toolbar.GetSizeTuple()
        graph_vbox.Add(self.toolbar)

        self.graph_panel.SetSizer(graph_vbox)
        graph_vbox.Fit(self)

        self.graph_canvas.mpl_connect('button_press_event', self.onclick)
        self.graph_canvas.mpl_connect('motion_notify_event', self.move_mouse)

        """
        Legend Panel Setup
        """
        title = wx.StaticText(self.legend_panel, wx.ID_ANY, 'Legend', style=wx.ALIGN_LEFT)
        font = wx.Font(28, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        title.SetFont(font)

        vbox_leg = wx.BoxSizer(wx.VERTICAL)
        vbox_leg.Add(title, flag=wx.CENTER)

        self.legend_panel.SetSizer(vbox_leg)
        self.legend_panel.Layout()

        """
        Menubar Setup
        """
        self.SetMenuBar(self.build_menu_bar())

        """
        WorldState Stuff
        """
        self.world.drop_down_species = self.drop_down_species
        self.world.drop_down_files = self.drop_down_files
        self.world.create_cell_segments_by_species = self.create_cell_segments_by_species
        self.world.create_cell_segments_by_file = self.create_cell_segments_by_file
        self.world.graph_canvas = self.graph_canvas
        self.world.play_animation = self.real_play_animation
        self.world.create_cell_segments_by_file = self.create_cell_segments_by_file
        self.world.create_cell_segments_by_species = self.create_cell_segments_by_species
        self.world.time_slider = self.slider_time
        self.world.anime_annotations_list = self.anime_annotations_list
        self.world.graph_axes = self.graph_axes
        self.world.graph_width = graph_width
        self.world.graph_height = graph_height
        self.world.legend = Legend(self.legend_panel)
        self.world.update_title = self.SetTitle
        self.world.get_title = self.GetTitle

        """
        Whole UI Setup
        """

        splitter_far_right.SplitVertically(splitter_horiz_middle, splitter_far_right_middle)
        splitter_horiz_middle.SplitHorizontally(splitter_vert_middle, self.animation_panel)
        splitter_vert_middle.SplitVertically(self.graph_panel, self.legend_panel)
        splitter_far_right_middle.SplitHorizontally(attachment_panel, annotation_panel)

        splitter_far_right.SetSashPosition((5 * self.world.dispW/6) + 10)
        splitter_vert_middle.SetSashPosition((4 * self.world.dispW/6) - 10)
        splitter_horiz_middle.SetSashPosition((graph_height * _DPI) + toolH + 5)
        splitter_far_right_middle.SetSashPosition(self.world.dispH/2)

        self.SetTitle(_TITLE)

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

        self.annotationm_toggle.Enable(state)

        self.undo_m.Enable(state)
        self.redo_m.Enable(state)

        self.normalise_m.Enable(state)
        self.export_data_m.Enable(state)

        self.share_session_m.Enable(state)

        if self.world.session_dict['tree_list']:
            self.btn_animate_play.Enable(state)
            self.slider_time.Enable(state)
            self.drop_down_species.Enable(state)
            self.drop_down_files.Enable(False)
            self.switch_animation_button.Enable(state)

            self.add_anime_annotation_button.Enable(state)
            self.delete_anime_annotation_button.Enable(state)
        else:
            self.btn_animate_play.Enable(False)
            self.slider_time.Enable(False)
            self.drop_down_species.Enable(False)
            self.drop_down_files.Enable(False)
            self.switch_animation_button.Enable(False)

            self.add_anime_annotation_button.Enable(False)
            self.delete_anime_annotation_button.Enable(False)

        self.add_files_button.Enable(state)
        self.open_files_button.Enable(state)

    def add_anime_annotation(self, e):
        self.world.session_dict['annotate_anime'] = True

        annotation_dialogue = AnnotationDialogue(None, title="Add Annotation")
        annotation_dialogue.ShowModal()
        annotation_dialogue.Destroy()

    def annotate_cell(self, e):
        """
        When we click on a cell viz panel
        """
        if self.world.session_dict['annotate_anime']:
            (x, y) = e.GetPosition()
            self.world.temp_anime_annotation.set_position((x, y))

            panel = e.GetEventObject()
            idx = int(panel.GetName())

            self.world.temp_anime_annotation.set_id(self.world.session_dict['cur_annotation_id'])
            self.world.session_dict['cur_annotation_id'] += 1

            self.world.add_anime_annotation(idx, self.world.temp_anime_annotation)

            self.world.lamport_clock += 1
            self.world.push_state()
            self.world.reorder(self.world.lamport_clock)

            self.world.client.add_anime_annotation((idx, self.world.temp_anime_annotation))

    def remove_anime_annotation(self, e):
        selected = self.anime_annotations_list.GetSelection()
        annotation = self.anime_annotations_list.GetString(selected)

        (a_id, text) = annotation.split(":")

        self.world.delete_anime_annotation(a_id)

        self.world.lamport_clock += 1
        self.world.push_state()
        self.world.reorder(self.world.lamport_clock)

        self.world.client.delete_anime_annotation(a_id)

    def move_mouse(self, event):
        """
        Handles the drawing of the arrow when deciding where to annotate
        """
        if self.world.draw_plot:
            if self.world.session_dict['click_one']:
                self.world.session_dict['temp_annotation'] = Annotation(self.world._ARROW, (self.world.session_dict['click_one_x'], self.world.session_dict['click_one_y']), (event.xdata, event.ydata))
            if self.world.session_dict['annotate']:
                self.world.session_dict['redraw_legend'] = False
                self.world.draw_plot.plot()
                self.world.session_dict['redraw_legend'] = True

    def open_attached_file(self, event):
        """
        Opening attached files, must be a better way of doing this
        """
        idx = self.attached_file_list.GetSelection()
        if platform.system() == "Linux":
            call(["gnome-open", self.world.session_dict['attached_file_locations'][idx]])
        else:
            call(["open", self.world.session_dict['attached_file_locations'][idx]])

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
        if event.xdata is not None and event.ydata is not None:
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
                    self.world.lamport_clock += 1
                    self.world.push_state()
                    self.world.reorder(self.world.lamport_clock)
                    return
            elif self.world.session_dict['annotation_mode'] == self.world._TEXT:
                if self.world.session_dict['annotate']:
                    self.world.draw_plot.annotate_text((event.xdata, event.ydata), text=self.world.session_dict['annotation_text'])
                    self.world.change_cursor(wx.CURSOR_ARROW)
                    self.world.session_dict['annotation_mode'] = self.world._NONE
                    self.world.lamport_clock += 1
                    self.world.push_state()
                    self.world.reorder(self.world.lamport_clock)
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
                    self.world.lamport_clock += 1
                    self.world.push_state()
                    self.world.reorder(self.world.lamport_clock)
                    return
            elif self.world.session_dict['annotation_mode'] == self.world._CIRCLE:
                if self.world.session_dict['annotate']:
                    self.world.draw_plot.annotate_circle((event.xdata, event.ydata), colour='black')
                    self.world.session_dict['annotation_mode'] = self.world._NONE
                    self.world.lamport_clock += 1
                    self.world.push_state()
                    self.world.reorder(self.world.lamport_clock)
                    return

    def right_click_handler(self, event):
        """
        Select existing annotations, offer to edit or delete
        """
        self.selected_annotation = None
        try:
            for annotation in self.world.session_dict['annotations']:
                dist = 1
                if annotation.type == self.world._TEXT_ARROW or annotation.type == self.world._ARROW:
                    dist = point_to_line_distance((annotation.x1/float(self.world.session_dict['max_time']),
                        annotation.y1/float(self.world.session_dict['max_height'])),
                        (annotation.x2/float(self.world.session_dict['max_time']), annotation.y2/float(self.world.session_dict['max_height'])),
                        (event.xdata/float(self.world.session_dict['max_time']), event.ydata/float(self.world.session_dict['max_height'])))
                else:
                    dist = euclid_distance((annotation.x1/float(self.world.session_dict['max_time']),
                        annotation.y1/float(self.world.session_dict['max_height'])),
                        (event.xdata/float(self.world.session_dict['max_time']), event.ydata/float(self.world.session_dict['max_height'])))
                if dist < 0.025:
                    if self.selected_annotation is None:
                        self.selected_annotation = annotation
                        break
            if self.selected_annotation is not None:
                self.selected_annotation.colour = 'red'
                refresh_plot()
                self.annotation_menu()
                refresh_plot()
                self.selected_annotation = None
            else:
                print "Missed annotation"
        except:
            print "Clicked outside of graph"

    def annotation_menu(self):
        annotate_menu = wx.Menu()

        m_edit_annotation = annotate_menu.Append(wx.ID_ANY, 'Edit')
        self.Bind(wx.EVT_MENU, self.edit_annotation_text, m_edit_annotation)

        m_delete_annotation = annotate_menu.Append(wx.ID_ANY, 'Delete')
        self.Bind(wx.EVT_MENU, self.delete_annotation, m_delete_annotation)

        self.graph_panel.PopupMenu(annotate_menu)
        annotate_menu.Destroy()

    def edit_annotation_text(self, event):
        self.get_label()

        self.world.update_annotation_text(self.selected_annotation.id, self.world.session_dict['annotation_text'])
        self.selected_annotation.colour = 'black'

        self.world.lamport_clock += 1
        self.world.push_state()
        self.world.reorder(self.world.lamport_clock)

        self.world.client.update_annotation(self.selected_annotation.id, self.selected_annotation.text)

    def get_label(self):
         dialog = wx.TextEntryDialog(None, "Please Enter a New Label.","Edit Annotation", "", style=wx.OK|wx.CANCEL)
         if dialog.ShowModal() == wx.ID_OK:
             self.world.session_dict['annotation_text'] = dialog.GetValue()

    def delete_annotation(self, event):
        self.world.delete_annotation(self.selected_annotation.id)

        self.world.lamport_clock += 1
        self.world.push_state()
        self.world.reorder(self.world.lamport_clock)

        self.world.client.delete_annotation(self.selected_annotation.id)

    def build_menu_bar(self):
        """
        The menu bar.
        Again could take this out to be its own class
        Need to organise the menu a bit better - look at mac style guidelines
        """
        menubar = wx.MenuBar()
        menubar.SetBackgroundColour(_BG_COLOUR)

        """
        File Menu
        """

        file_menu = wx.Menu()

        self.filem_new_session = file_menu.Append(wx.ID_NEW, '&New Session')
        self.filem_save_session = file_menu.Append(wx.ID_ANY, '&Save Session')
        self.filem_load_session  = file_menu.Append(wx.ID_ANY, '&Load Session')
        file_menu.AppendSeparator()
        self.filem_open_results_save_plot = file_menu.Append(wx.ID_SAVE, 'Export Graph')

        menubar.Append(file_menu, '&File')

        self.Bind(wx.EVT_MENU, self.new_session, self.filem_new_session)
        self.Bind(wx.EVT_MENU, self.save_session, self.filem_save_session)
        self.Bind(wx.EVT_MENU, self.load_session, self.filem_load_session)
        self.Bind(wx.EVT_MENU, self.on_save_plot, self.filem_open_results_save_plot)

        """
        Preferences Menu
        """

        preferences_menu = wx.Menu()

        self.annotationm_toggle = preferences_menu.AppendCheckItem(wx.ID_ANY, '&Annotations')
        self.annotationm_toggle.Check()

        menubar.Append(preferences_menu, '&Preferences')

        self.Bind(wx.EVT_MENU, self.toggle_annotations, self.annotationm_toggle)

        """
        Edit Menu
        """

        edit_menu = wx.Menu()

        self.undo_m = edit_menu.Append(wx.ID_ANY, '&Undo')
        self.redo_m = edit_menu.Append(wx.ID_ANY, '&Redo')

        menubar.Append(edit_menu, '&Edit')

        self.Bind(wx.EVT_MENU, self.undo, self.undo_m)
        self.Bind(wx.EVT_MENU, self.redo, self.redo_m)

        """
        Data Menu
        """

        data_menu = wx.Menu()

        self.normalise_m = data_menu.AppendCheckItem(wx.ID_ANY, '&Normalise')
        self.export_data_m = data_menu.Append(wx.ID_ANY, '&Export Data')

        self.Bind(wx.EVT_MENU, self.normalise_data, self.normalise_m)
        self.Bind(wx.EVT_MENU, self.export_data, self.export_data_m)

        menubar.Append(data_menu, '&Data')

        """
        Networking Menu
        """

        networking_menu = wx.Menu()

        self.share_session_m = networking_menu.Append(wx.ID_ANY, '&Share Session')
        self.Bind(wx.EVT_MENU, self.start_rpc_server, self.share_session_m)

        self.join_session_m = networking_menu.Append(wx.ID_ANY, '&Join Session')
        self.Bind(wx.EVT_MENU, self.join_rpc_server, self.join_session_m)

        menubar.Append(networking_menu, '&Networking')

        return menubar

    def start_rpc_server(self, e):
        wx.MessageBox("Run 'sudo ifconfig' and send ip address to collaborator.", 'Info', wx.OK | wx.ICON_INFORMATION)

        server_thread = Thread(target=self.run_server, args=(8000,))
        server_thread.start()

    def run_server(self, port):
        self.share_session_m.Enable(False)
        self.join_session_m.Enable(False)
        self.world.server = French75Server(port)

    def join_rpc_server(self, e):
        dialog = wx.TextEntryDialog(None, "Please Enter Server IP Address","Text Entry", "", style=wx.OK|wx.CANCEL)

        if dialog.ShowModal() == wx.ID_OK:
            dialog2 = wx.TextEntryDialog(None, "Please Enter Your IP Address", "Text Entry", "", style=wx.OK|wx.CANCEL)

            if dialog2.ShowModal() == wx.ID_OK:
                self.share_session_m.Enable(False)
                self.join_session_m.Enable(False)
                client_thread = Thread(target=self.run_client, args=(dialog.GetValue(), dialog2.GetValue()))
                client_thread.start()

                server_thread = Thread(target=self.run_server, args=(8001,))
                server_thread.start()

    def run_client(self, server_ip, my_ip):
        self.world.client = French75Client(server_ip, 8000)
        self.world.client.start_partner_client(my_ip)
        success = self.world.client.request_session()
        if success:
            self.sessiony_stuff()

    def normalise_data(self, event):
        self.toggle_param('normalised')

    def export_data(self, event):
        titles = []
        data_arrays = []
        for file_name in self.world.session_dict['lines'].keys():
            for species in self.world.session_dict['lines'][file_name].keys():
                titles.append(species)
                data_arrays.append(self.world.session_dict['lines'][file_name][species].original_results)
                titles.append(species + "-normalised")
                data_arrays.append(self.world.session_dict['lines'][file_name][species].normalised_results)
        out_str = ""
        out_str += ','.join(titles)
        out_str += "\n"
        for line in zip(*data_arrays):
            out_str += ','.join(map(str,line))
            out_str += "\n"
        file_choices = "CSV (*.csv)|*.csv"

        dlg = wx.FileDialog(
            self,
            message="Export Data as...",
            defaultDir=os.getcwd(),
            defaultFile="exported_data.csv",
            wildcard=file_choices,
            style=wx.SAVE)

        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            with open(path, 'wb') as f:
                f.write(out_str)
            self.SetTitle(_TITLE)
        else:
            dlg.Destroy()

    def undo(self, event):
        self.world.undo()
        self.world.client.undo()

    def redo(self, event):
        self.world.redo()
        self.world.client.redo()

    def toggle_xkcd(self, event):
        self.toggle_param('xkcd')
        matplotlib.pyplot.xkcd()

    def toggle_annotations(self, event):
        self.toggle_param('draw_annotations')
        print self.world.session_dict['draw_annotations']

    def toggle_param(self, param):
        self.world.session_dict[param] = not self.world.session_dict[param]

        self.world.lamport_clock += 1
        self.world.push_state()
        self.world.reorder(self.world.lamport_clock)

        self.world.client.toggle_param(param, self.world.session_dict[param])
        refresh_plot()

    def new_session(self, e):
        """
        Session starter dialogue
        """
        self.world.temp_session_dict = self.world.session_dict
        self.world.reset_session()
        self.world.session_dict['lines'] = {}
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

        self.slider_time.SetMax(self.world.session_dict['max_time'])

        if self.world.session_dict['tree_list']:
            for species in self.list_of_species():
                self.drop_down_species.Append(species)
            for file_name in self.world.session_dict['results'].keys():
                self.drop_down_files.Append(file_name)

            self.drop_down_species.SetSelection(0)
            self.drop_down_files.SetSelection(0)

            self.create_cell_segments_by_file(self.drop_down_files.GetSelection())
        self.world.populate_anime_annotation_lb()

        self.world.push_state()
        self.world.lamport_clock += 1
        self.enable_all(True)

    def change_animation_species(self, e):
        n = self.drop_down_species.GetSelection()
        self.create_cell_segments_by_file(n)
        self.world.client.change_animation_species(n)

    def change_animation_file(self, e):
        n = self.drop_down_files.GetSelection()
        self.create_cell_segments_by_species(n)
        self.world.client.change_animation_file(n)

    def create_cell_segments_by_file(self, n):
        self.drop_down_species.SetSelection(n)
        (a_width, a_height) = self.animation_panel.GetSize()

        for child in self.animation_panel.GetChildren():
            try:
                int(child.GetName())
                child.Destroy()
            except:
                pass

        self.world.panels = []
        panel_vboxes = []
        self.world.cell_segments = []

        #TODO: Fix these magic numbers
        a = 10
        b = (a_height * 0.7) - 10
        c = (a_height * 0.7) - 20
        d = 0

        for i, file_name in enumerate(sorted(self.world.session_dict['results'].keys())):
            small_vbox = wx.BoxSizer(wx.VERTICAL)
            panel_vboxes.append(small_vbox)

            title = wx.StaticText(self.animation_panel, -1, file_name, name=str(i))
            small_vbox.Add(title,0,wx.EXPAND|wx.ALL,border=2)

            panel = wx.Panel(self.animation_panel, -1,size=(a_height*0.7,a_height*0.7), name=str(i))
            panel.SetBackgroundColour('white')
            panel.Bind(wx.EVT_PAINT, self.animate_cell)
            panel.Bind(wx.EVT_LEFT_UP, self.annotate_cell)
            small_vbox.Add(panel,0,wx.EXPAND|wx.ALL,border=2)
            self.world.panels.append(panel)

            self.animation_panels_hbox.Add(small_vbox,0,wx.EXPAND|wx.ALL,border=2)

            self.world.cell_segments.append(CellSegment((a, b), c, d, file_name, self.drop_down_species.GetStringSelection()))

        self.animation_panel.Layout()
        self.animation_panel.SetupScrolling(scroll_y=False)

        for panel in self.world.panels:
            panel.Refresh()

    def create_cell_segments_by_species(self, n):
        self.drop_down_files.SetSelection(n)

        (a_width, a_height) = self.animation_panel.GetSize()
        for child in self.animation_panel.GetChildren():
            try:
                int(child.GetName())
                child.Destroy()
            except:
                pass
        self.world.panels = []
        panel_vboxes = []
        self.world.cell_segments = []

        #TODO: Fix these magic numbers
        a = 10
        b = (a_height * 0.7) - 10
        c = (a_height * 0.7) - 20
        d = 0
        for i, species_name in enumerate(sorted(self.list_of_species())):
            if species_name != "Time":
                small_vbox = wx.BoxSizer(wx.VERTICAL)
                panel_vboxes.append(small_vbox)

                title = wx.StaticText(self.animation_panel, -1, species_name, name=str(i))
                small_vbox.Add(title,0,wx.EXPAND|wx.ALL,border=2)

                panel = wx.Panel(self.animation_panel, -1,size=(a_height*0.7,a_height*0.7), name=str(i))
                panel.SetBackgroundColour('white')
                panel.Bind(wx.EVT_PAINT, self.animate_cell)
                self.world.panels.append(panel)
                small_vbox.Add(panel,0,wx.EXPAND|wx.ALL,border=2)

                self.animation_panels_hbox.Add(small_vbox,0,wx.EXPAND|wx.ALL,border=2)
                self.world.cell_segments.append(CellSegment((a, b), c, d, self.drop_down_files.GetStringSelection(), species_name.split("@")[0]))

        self.animation_panel.Layout()
        self.animation_panel.SetupScrolling(scroll_y=False)

        for panel in self.world.panels:
            panel.Refresh()

    def switch_animation(self, e):
        if self.drop_down_species.IsEnabled():
            self.drop_down_species.Enable(False)
            self.drop_down_files.Enable(True)
            self.change_animation_file(None)
        else:
            self.drop_down_species.Enable(True)
            self.drop_down_files.Enable(False)
            self.change_animation_species(None)

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
            message="Choose session to load...",
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
        self.world.client.play_animation()
        self.real_play_animation()

    def real_play_animation(self):
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

    def animate_cell(self, e):
        """
        called when the animation pane is refreshed. -- OnPaint
        pane is refreshed by animate()
        update the position of the vertical line.  Draw each of the cell segments
        """
        wx.CallAfter(self.world.draw_plot.vertical_line)
        panel = e.GetEventObject()
        idx = int(panel.GetName())
        dc2 = wx.PaintDC(panel)
        self.world.cell_segments[idx].paint(dc2, idx)

    def animate(self, n):
        """
        Run by the thread
        Check the time and whether we are paused or not, if not then update the
        clock and redraw
        """
        while self.world.session_dict['clock'] < self.world.session_dict['max_time']:
            while self.world.session_dict['clock_pause']:
                pass
            time.sleep(n)
            self.world.session_dict['clock'] += self.world.session_dict['clock_increment']
            self.slider_time.SetValue(self.world.session_dict['clock'])
            for panel in self.world.panels:
                panel.Refresh()

        self.slider_time.SetValue(self.world.session_dict['max_time'])
        self.change_button_text('Play')
        self.world.session_dict['start_playing'] = False

    def on_save_plot(self, event):
        """
        Save the graph
        """
        file_choices = "PNG (*.png)|*.png"

        dlg = wx.FileDialog(
            self,
            message="Export plot as...",
            defaultDir=os.getcwd(),
            defaultFile="plot.png",
            wildcard=file_choices,
            style=wx.SAVE)

        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.world.draw_plot.mpl_legend = True
            refresh_plot()
            self.graph_canvas.print_figure(path, dpi=_DPI)
            self.world.draw_plot.mpl_legend = False
            refresh_plot()

    def move_animation(self, e):
        """
        Bound to the slider when you move it -- updates the session clock
        """
        self.world.session_dict['clock'] = self.slider_time.GetValue()
        for segment in self.world.cell_segments:
            segment.update_clock()

    def released_slider(self, e):
        self.world.client.set_clock()

if __name__ == '__main__':
    app = wx.App()
    gui = French75(None)
    gui.Show()
    app.MainLoop()
    app.Destroy()
