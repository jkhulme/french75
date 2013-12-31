import wx
from worldstate import WorldState
from utils import open_results_file
import wx.wizard as wizmod
from line import Line
from validators import TextNotEmptyValidator

_PADDING = 5


class SessionWizard(wx.wizard.Wizard):
    '''Add pages to this wizard object to make it useful.'''
    def __init__(self, title, img_filename=""):
        wx.wizard.Wizard.__init__(self, None, -1, title)

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

        page1 = wizard_page(self, 'Enter Title')  # Create a first page
        self.title_text = wx.TextCtrl(page1, -1, size=(300, -1), validator = TextNotEmptyValidator())
        page1.add_widget(self.title_text)
        self.add_page(page1)

        page2 = wizard_page(self, 'Select Results Files')
        self.file_list = wx.ListBox(page2, -1, size=(300, -1), style=wx.LB_MULTIPLE)
        page2.add_widget(self.file_list)
        file_toolbar = wx.BoxSizer(wx.HORIZONTAL)
        btn_add_file = wx.Button(page2, -1, "Add")
        btn_add_file.Bind(wx.EVT_BUTTON, self.add_files)
        btn_rem_file = wx.Button(page2, -1, "Remove")
        btn_rem_file.Bind(wx.EVT_BUTTON, self.remove_files)
        file_toolbar.Add(btn_add_file)
        file_toolbar.Add(btn_rem_file)
        page2.add_widget(file_toolbar)
        self.add_page(page2)

        page3 = wizard_page(self, 'Select Model File')
        self.model_list = wx.ListBox(page3, -1, size=(300, -1), style=wx.LB_SINGLE)
        model_button = wx.Button(page3, -1, "Select")
        model_button.Bind(wx.EVT_BUTTON, self.select_model)
        page3.add_widget(self.model_list)
        page3.add_widget(model_button)
        self.add_page(page3)

        page4 = wizard_page(self, 'Perinuclear Species')
        self.species_list_peri = wx.CheckListBox(page4, -1, size=(200, -1), style=wx.LB_MULTIPLE)
        page4.add_widget(self.species_list_peri)
        self.add_page(page4)

        page5 = wizard_page(self, 'Cytoplasmic Species')
        self.species_list_mid = wx.CheckListBox(page5, -1, size=(200, -1), style=wx.LB_MULTIPLE)
        page5.add_widget(self.species_list_mid)
        self.add_page(page5)

        page6 = wizard_page(self, 'Cell Membrane Species')
        self.species_list_api = wx.CheckListBox(page6, -1, size=(200, -1), style=wx.LB_MULTIPLE)
        page6.add_widget(self.species_list_api)
        self.add_page(page6)

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
        open_results_file(self)
        for key in self.world.session_dict['results'].keys():
            self.species_dict[key] = []
            for species in self.world.session_dict['results'][key].keys():
                if species != 'Time':
                    self.species_dict[key].append(species)
            self.populate_species_lists()
            self.chosen_paths.append(key)
            self.file_list.Append(key)

    def remove_files(self, e):
        old_paths = [path for i, path in enumerate(self.chosen_paths) if i in self.file_list.GetSelections()]
        self.chosen_paths = [path for i, path in enumerate(self.chosen_paths) if i not in self.file_list.GetSelections()]
        for path in old_paths:
            del self.species_dict[path.split('/')[-1]]
        self.file_list.Clear()
        for path in self.chosen_paths:
            self.file_list.Append(path.split('/')[-1])
        self.populate_species_lists()

    def populate_species_lists(self):
        self.species_list_peri.Clear()
        self.species_list_mid.Clear()
        self.species_list_api.Clear()
        for key in self.species_dict.keys():
            for species in self.species_dict[key]:
                self.species_list_peri.Append(species)
                self.species_list_mid.Append(species)
                self.species_list_api.Append(species)

    def select_model(self, e):
        file_chooser = wx.FileDialog(
            self,
            message="Choose a file",
            wildcard="*.biopepa",
            style=wx.OPEN | wx.CHANGE_DIR)
        if file_chooser.ShowModal() == wx.ID_OK:
            path = file_chooser.GetPaths()[0]
            self.model_list.Append(path.split('/')[-1])
            file_chooser.Destroy()
        else:
            file_chooser.Destroy()

    def Destroy(self):
        self.Close()

    def cancel_wizard(self, e):
        print "Cancelling the wizard"
        if self.state != self._FINISHED:
            self.state = self._CANCELLED
        self.Destroy()

    def finish_wizard(self, e):
        print "Finishing the wizard"
        self.state = self._FINISHED
        self.Destroy()

    def parse_species(self):
        self.world.session_dict['species_dict'] = {}
        inner = self.species_list_peri.GetCheckedStrings()[0]
        middle = self.species_list_mid.GetCheckedStrings()[0]
        outer = self.species_list_api.GetCheckedStrings()[0]
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
        self.world.session_dict['lines'] = self.world.session_dict['lines']


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


