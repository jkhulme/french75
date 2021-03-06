import wx
from worldstate import WorldState
from utils import open_results_file
import wx.wizard as wizmod
from line import Line
from validators import TextNotEmptyValidator, ResultsListNotEmptyValidator
from biopepa_model_parser import Biopepa_Model_Parser
from cell_segments2 import CellSegments2

_PADDING = 5


class SessionWizard(wx.wizard.Wizard):

    """
    Using a wizard to guide the user through the process of starting a new
    session easier.  Also looks better than a long scrolling list of things.
    """

    def __init__(self, title, img_filename=""):
        wx.wizard.Wizard.__init__(self, None, -1, title)

        self._STARTED = 0
        self._FINISHED = 1
        self._CANCELLED = 2

        self.pages = []
        self.state = self._STARTED
        self.tree = None

        self.Bind(wizmod.EVT_WIZARD_CANCEL, self.cancel_wizard)
        self.Bind(wizmod.EVT_WIZARD_FINISHED, self.finish_wizard)

        self.chosen_paths = []
        self.species_dict = {}

        #WorldState.Instance() = WorldState.Instance()
        height, width = self.GetSize()

        #PAGE 1
        page1 = wizard_page(self, 'Enter Title')  # Create a first page
        title_label = wx.StaticText(page1, wx.ID_ANY, '', style=wx.ALIGN_LEFT)
        self.title_text = wx.TextCtrl(page1, -1, size=(300, -1), validator = TextNotEmptyValidator(title_label))
        page1.add_widget(self.title_text)
        page1.add_widget(title_label)
        line1 = wx.StaticLine(page1)
        page1.add_widget(line1)
        p1_help_text = "This will be used as the title of your graph, and will appear on any pictures of the graph that are saved."
        page1_help = wx.StaticText(page1, wx.ID_ANY, p1_help_text, style=wx.ALIGN_LEFT)
        page1_help.Wrap(width)
        page1.add_widget(page1_help)
        self.add_page(page1)

        #PAGE 2
        page2 = wizard_page(self, 'Select Results Files')
        results_label = wx.StaticText(page2, wx.ID_ANY, '', style=wx.ALIGN_LEFT)
        self.file_list = wx.ListBox(page2, -1, size=(300, -1), style=wx.LB_MULTIPLE, validator=ResultsListNotEmptyValidator(results_label))
        page2.add_widget(self.file_list)
        file_toolbar = wx.BoxSizer(wx.HORIZONTAL)
        btn_add_file = wx.Button(page2, -1, "Add")
        btn_add_file.Bind(wx.EVT_BUTTON, self.add_files)
        btn_rem_file = wx.Button(page2, -1, "Remove")
        btn_rem_file.Bind(wx.EVT_BUTTON, self.remove_files)
        file_toolbar.Add(btn_add_file, 0, wx.ALL, 5)
        file_toolbar.Add(btn_rem_file, 0, wx.ALL, 5)
        page2.add_widget(file_toolbar, expand=False)

        page2.add_widget(results_label)

        line2 = wx.StaticLine(page2)
        page2.add_widget(line2)

        p2_help_text = "Results files are the CSVs output from BioPEPA.\nMultiple files can be selected."
        page2_help = wx.StaticText(page2, wx.ID_ANY, p2_help_text, style=wx.ALIGN_LEFT)
        page2_help.Wrap(width)
        page2.add_widget(page2_help)

        self.add_page(page2)

        #PAGE 3
        page3 = wizard_page(self, 'Select Model File')
        self.model_list = wx.ListBox(page3, -1, size=(300, -1), style=wx.LB_SINGLE)
        model_button = wx.Button(page3, -1, "Select")
        model_button.Bind(wx.EVT_BUTTON, self.select_model)
        page3.add_widget(self.model_list)
        page3.add_widget(model_button, expand=False)

        line3 = wx.StaticLine(page3)
        page3.add_widget(line3)

        p3_help_text = "Model files are the .biopepa files.  They are used for visualising species moving through the cell.\n\nModel files are not required."
        page3_help = wx.StaticText(page3, wx.ID_ANY, p3_help_text, style=wx.ALIGN_LEFT)
        page3_help.Wrap(width)
        page3.add_widget(page3_help)

        self.add_page(page3)

        #PAGE 4
        page4 = wizard_page(self, 'Species Locations')
        self.file_dd = wx.ComboBox(page4, -1, style=wx.CB_READONLY)
        self.file_dd.Bind(wx.EVT_COMBOBOX, self.change_file)
        self.species_dd = wx.ComboBox(page4, -1, style=wx.CB_READONLY)
        self.species_dd.Bind(wx.EVT_COMBOBOX, self.change_species)

        self.location_panel = wx.Panel(page4, -1, size=(1000000, 1000000))
        page4.add_widget(self.file_dd)
        page4.add_widget(self.species_dd)

        p4_help_text = "Green: Present at location\nWhite: Absent at location"
        page4_help = wx.StaticText(page4, wx.ID_ANY, p4_help_text, style=wx.ALIGN_LEFT)
        page4_help.Wrap(width)
        page4.add_widget(page4_help)

        page4.add_widget(self.location_panel)
        page4.Bind(wizmod.EVT_WIZARD_PAGE_SHOWN, self.page4_location_panel_size)

        self.add_page(page4)

    def page4_location_panel_size(self, e):
        (width, height) = self.location_panel.GetSize()
        if self.tree:
            self.cell = CellSegments2(self.tree, (width, height))
            self.location_panel.Bind(wx.EVT_PAINT, self.draw_cell)
            self.location_panel.Refresh()

    def draw_cell(self, e):
        dc = wx.PaintDC(self.location_panel)
        self.cell.paint(dc, self.get_current_species_locations())

    def get_current_species_locations(self):
        return self.species_dict[self.file_dd.GetValue()][self.species_dd.GetValue()]

    def add_page(self, page):
        '''Add a wizard page to the list.'''
        if self.pages:
            previous_page = self.pages[-1]
            page.SetPrev(previous_page)
            previous_page.SetNext(page)
        self.pages.append(page)

    def run(self):
        self.RunWizard(self.pages[0])

    def add_files(self, e):
        """
        Results files.  There can be many, they can be added in multiple goes
        """
        open_results_file(self)
        for key in WorldState.Instance().session_dict['results'].keys():
            self.species_dict[key] = {}
            for species in WorldState.Instance().session_dict['results'][key].keys():
                if species != 'Time':
                    try:
                        (name, location) = species.split("@")
                    except:
                        (name, location) = (species, "whole_cell")
                    if name in self.species_dict[key]:
                        self.species_dict[key][name].append(location)
                    else:
                        self.species_dict[key][name] = [location]
            self.populate_file_dd_list()
            self.chosen_paths.append(key)
            self.file_list.Append(key)

    def remove_files(self, e):
        """
        Again results files, because there can be many and they can be removed
        in multiple goes
        """
        old_paths = [path for i, path in enumerate(self.chosen_paths) if i in self.file_list.GetSelections()]
        self.chosen_paths = [path for i, path in enumerate(self.chosen_paths) if i not in self.file_list.GetSelections()]
        for path in old_paths:
            del self.species_dict[path.split('/')[-1]]
        self.file_list.Clear()
        for path in self.chosen_paths:
            self.file_list.Append(path.split('/')[-1])
        self.populate_file_dd_list()

    def populate_file_dd_list(self):
        """
        Get a list of all species, it is called whenever results files are
        added or removed
        """
        self.file_dd.Clear()
        for key in self.species_dict.keys():
            self.file_dd.Append(key)
            self.file_dd.SetSelection(0)
        self.populate_species_dd_list()

    def populate_species_dd_list(self):
        self.species_dd.Clear()
        for species in self.species_dict[self.file_dd.GetValue()]:
            self.species_dd.Append(species)
            self.species_dd.SetSelection(0)

    def change_file(self, e):
        self.populate_species_dd_list()
        self.location_panel.Refresh()

    def change_species(self, e):
        self.location_panel.Refresh()

    def select_model(self, e):
        """
        Only one
        """
        file_chooser = wx.FileDialog(
            self,
            message="Choose a file",
            wildcard="*.biopepa",
            style=wx.OPEN | wx.CHANGE_DIR)
        if file_chooser.ShowModal() == wx.ID_OK:
            path = file_chooser.GetPaths()[0]
            self.model_list.Append(path.split('/')[-1])
            self.model_parser = Biopepa_Model_Parser()
            self.model_parser.parse(path)
            self.tree = self.model_parser.build_graph()
            file_chooser.Destroy()
        else:
            file_chooser.Destroy()

    def Destroy(self):
        self.Close()

    def cancel_wizard(self, e):
        """
        For some reason, finishing normally also comes in here
        """
        if self.state != self._FINISHED:
            self.state = self._CANCELLED
        self.Destroy()

    def finish_wizard(self, e):
        self.state = self._FINISHED
        self.Destroy()

    def parse_species(self):
        WorldState.Instance().session_dict['species_dict'] = self.species_dict

        #Create a line for each result
        for result in WorldState.Instance().session_dict['results']:
            results_dict = WorldState.Instance().session_dict['results'][result]
            WorldState.Instance().session_dict['lines'][result] = {}
            for key in results_dict:
                if (not key == 'Time'):
                    WorldState.Instance().session_dict['lines'][result][key] = Line(
                                                     results_dict[key],
                                                     results_dict['Time'],
                                                     result, key,
                                                     WorldState.Instance().choose_colour(),
                                                     WorldState.Instance().graph_width,
                                                     WorldState.Instance().graph_height,
                                                     WorldState.Instance().session_dict['xmin'],
                                                     WorldState.Instance().session_dict['xmax'],
                                                     WorldState.Instance().session_dict['ymin'],
                                                     WorldState.Instance().session_dict['ymax'])


class wizard_page(wizmod.PyWizardPage):
    """
    Taken from wxPython documentation
    """
    ''' An extended panel obj with a few methods to keep track of its siblings.
        This should be modified and added to the wizard.  Season to taste.'''
    def __init__(self, parent, title):
        wx.wizard.PyWizardPage.__init__(self, parent)
        self.next = self.prev = None
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        title = wx.StaticText(self, -1, title)
        title.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.sizer.AddWindow(title, 0, wx.ALIGN_LEFT|wx.ALL, _PADDING)
        self.sizer.AddWindow(wx.StaticLine(self, -1), 0, wx.EXPAND|wx.ALL, _PADDING)
        self.SetSizer(self.sizer)

    def add_widget(self, stuff, expand=True):
        '''Add additional widgets to the bottom of the page'''
        if expand:
            self.sizer.Add(stuff, 0, wx.EXPAND|wx.ALL, _PADDING)
        else:
            self.sizer.Add(stuff, 0, wx.ALL|wx.ALIGN_CENTRE, _PADDING)

    def SetNext(self, next):
        '''Set the next page'''
        self.next = next

    def SetPrev(self, prev):
        '''Set the previous page'''
        self.prev = prev

    def GetNext(self):
        '''Return the next page'''
        return self.next

    def GetPrev(self):
        '''Return the previous page'''
        return self.prev


