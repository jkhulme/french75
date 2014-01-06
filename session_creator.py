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

        #These states are so that I know what has or hasn't been done on
        #completion or cancellation.  More will be added.
        self._STARTED = 0
        self._FINISHED = 1
        self._CANCELLED = 2

        self.pages = []
        self.state = self._STARTED

        self.Bind(wizmod.EVT_WIZARD_CANCEL, self.cancel_wizard)
        self.Bind(wizmod.EVT_WIZARD_FINISHED, self.finish_wizard)

        self.chosen_paths = []
        self.species_dict = {}

        self.world = WorldState.Instance()

        #PAGE 1
        page1 = wizard_page(self, 'Enter Title')  # Create a first page
        title_label = wx.StaticText(page1, wx.ID_ANY, '', style=wx.ALIGN_LEFT)
        self.title_text = wx.TextCtrl(page1, -1, size=(300, -1), validator = TextNotEmptyValidator(title_label))
        page1.add_widget(self.title_text)
        page1.add_widget(title_label)
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
        file_toolbar.Add(btn_add_file)
        file_toolbar.Add(btn_rem_file)
        page2.add_widget(file_toolbar)

        page2.add_widget(results_label)
        self.add_page(page2)

        #PAGE 3
        page3 = wizard_page(self, 'Select Model File')
        self.model_list = wx.ListBox(page3, -1, size=(300, -1), style=wx.LB_SINGLE)
        model_button = wx.Button(page3, -1, "Select")
        model_button.Bind(wx.EVT_BUTTON, self.select_model)
        page3.add_widget(self.model_list)
        page3.add_widget(model_button)
        self.add_page(page3)

        #PAGE 4
        page4 = wizard_page(self, 'Species Locations')
        self.file_dd = wx.ComboBox(page4, -1, style=wx.CB_READONLY)
        self.file_dd.Bind(wx.EVT_COMBOBOX, self.change_file)
        self.species_dd = wx.ComboBox(page4, -1, style=wx.CB_READONLY)

        self.location_panel = wx.Panel(page4, -1, size=(1000000, 1000000))
        self.location_panel.SetBackgroundColour('white')
        #self.species_list_peri = wx.CheckListBox(page4, -1, size=(200, -1), style=wx.LB_MULTIPLE)
        page4.add_widget(self.file_dd)
        page4.add_widget(self.species_dd)
        page4.add_widget(self.location_panel)
        page4.Bind(wizmod.EVT_WIZARD_PAGE_SHOWN, self.page4_location_panel_size)
        #page4.add_widget(self.species_list_peri)
        self.add_page(page4)

        """
        #PAGE 5
        page5 = wizard_page(self, 'Cytoplasmic Species')
        self.species_list_mid = wx.CheckListBox(page5, -1, size=(200, -1), style=wx.LB_MULTIPLE)
        page5.add_widget(self.species_list_mid)
        self.add_page(page5)

        #PAGE 6
        page6 = wizard_page(self, 'Cell Membrane Species')
        self.species_list_api = wx.CheckListBox(page6, -1, size=(200, -1), style=wx.LB_MULTIPLE)
        page6.add_widget(self.species_list_api)
        self.add_page(page6)
        """

    def page4_location_panel_size(self, e):
        (width, height) = self.location_panel.GetSize()
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
        for key in self.world.session_dict['results'].keys():
            self.species_dict[key] = {}
            for species in self.world.session_dict['results'][key].keys():
                print species
                if species != 'Time':
                    try:
                        (name, location) = species.split("@")
                        print name, location
                    except:
                        (name, location) = (species, "whole_cell")
                    if name in self.species_dict[key]:
                        self.species_dict[key][name].append(location[:-1])
                    else:
                        self.species_dict[key][name] = [location[:-1]]
            self.populate_file_dd_list()
            self.chosen_paths.append(key)
            self.file_list.Append(key)
        print self.species_dict

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
        """
        self.species_list_peri.Clear()
        self.species_list_mid.Clear()
        self.species_list_api.Clear()
        """
        self.file_dd.Clear()
        for key in self.species_dict.keys():
            self.file_dd.Append(key)
        self.file_dd.SetSelection(0)

        self.populate_species_dd_list()
        """
            self.species_list_peri.Append(species)
            self.species_list_mid.Append(species)
            self.species_list_api.Append(species)
        """

    def populate_species_dd_list(self):
        self.species_dd.Clear()
        for species in self.species_dict[self.file_dd.GetValue()]:
            self.species_dd.Append(species)
        self.species_dd.SetSelection(0)

    def change_file(self, e):
        self.populate_species_dd_list()

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
        """
        Need to go over this again and work out what it is doing
        """
        self.world.session_dict['species_dict'] = {}
        inner = self.species_list_peri.GetCheckedStrings()
        middle = self.species_list_mid.GetCheckedStrings()
        outer = self.species_list_api.GetCheckedStrings()
        if len(inner) > 0 and len(middle) > 0 and len(outer) > 0:
            inner = inner[0]
            middle = middle[0]
            outer = outer[0]
            loc_flag = 0
            for file_name in self.world.session_dict['results'].keys():
                for result in self.world.session_dict['results'][file_name].keys():
                    if not result == "Time":
                        if result == inner:
                            loc_flag = 1
                        elif result == middle:
                            loc_flag = 2
                        elif result == outer:
                            loc_flag = 3
                        try:
                            (name, loc) = result.split("@")
                            (species, location, flag) = (name, loc, loc_flag)
                        except:
                            (species, location, flag) = (result, None, loc_flag)

                        if species not in self.world.session_dict['species_dict'].keys():
                            self.world.session_dict['species_dict'][species] = [(species,location,flag)]
                        else:
                            self.world.session_dict['species_dict'][species].append((species,location,flag))

        #Create a line for each result
        for result in self.world.session_dict['results']:
            results_dict = self.world.session_dict['results'][result]
            self.world.session_dict['lines'][result] = {}
            for key in results_dict:
                if (not key == 'Time'):
                    self.world.session_dict['lines'][result][key] = Line(
                                                     results_dict[key],
                                                     results_dict['Time'],
                                                     result, key,
                                                     self.world.choose_colour())


class wizard_page(wizmod.PyWizardPage):
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

    def add_widget(self, stuff):
        '''Add additional widgets to the bottom of the page'''
        self.sizer.Add(stuff, 0, wx.EXPAND|wx.ALL, _PADDING)

    #Would like to get rid of the following methods, but they seem to be needed by some parent code
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


