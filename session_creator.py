import wx
from worldstate import WorldState
from utils import open_results_file
import wx.wizard as wizmod


class SessionDialog(wx.Dialog):

    def __init__(self, *args, **kw):
        super(SessionDialog, self).__init__(*args, **kw)

        self.chosen_paths = []
        self.species_dict = {}

        self.world = WorldState.Instance()

        session_panel = wx.Panel(self)
        panel_vbox = wx.BoxSizer(wx.VERTICAL)

        self.title_text = wx.TextCtrl(session_panel, -1, size=(300, -1))
        title_label = wx.StaticText(session_panel, -1, "Title: ")
        title_sizer = wx.BoxSizer(wx.HORIZONTAL)
        title_sizer.Add(title_label)
        title_sizer.Add(self.title_text)
        panel_vbox.Add(title_sizer, flag=wx.ALIGN_CENTER | wx.TOP, border=7)

        self.file_list = wx.ListBox(session_panel, -1, size=(300, -1), style=wx.LB_MULTIPLE)
        file_label = wx.StaticText(session_panel, -1, "Results: ")
        file_sizer = wx.BoxSizer(wx.HORIZONTAL)
        file_sizer.Add(file_label)
        file_sizer.Add(self.file_list)
        panel_vbox.Add(file_sizer, flag=wx.ALIGN_CENTER | wx.TOP, border=7)

        file_toolbar = wx.BoxSizer(wx.HORIZONTAL)
        btn_add_file = wx.Button(session_panel, -1, "Add")
        btn_add_file.Bind(wx.EVT_BUTTON, self.add_files)
        btn_rem_file = wx.Button(session_panel, -1, "Remove")
        btn_rem_file.Bind(wx.EVT_BUTTON, self.remove_files)
        file_toolbar.Add(btn_add_file)
        file_toolbar.Add(btn_rem_file)
        panel_vbox.Add(file_toolbar, flag=wx.ALIGN_CENTER | wx.TOP, border=7)

        self.model_list = wx.ListBox(session_panel, -1, size=(300, -1), style=wx.LB_SINGLE)
        model_label = wx.StaticText(session_panel, -1, "Model: ")
        model_sizer = wx.BoxSizer(wx.HORIZONTAL)
        model_sizer.Add(model_label)
        model_sizer.Add(self.model_list)
        panel_vbox.Add(model_sizer, flag=wx.ALIGN_CENTER | wx.TOP, border=7)
        model_button = wx.Button(session_panel, -1, "Select")
        model_button.Bind(wx.EVT_BUTTON, self.select_model)
        panel_vbox.Add(model_button, flag=wx.ALIGN_CENTER | wx.TOP, border=7)

        species_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.species_list_peri = wx.CheckListBox(session_panel, -1, size=(200, -1), style=wx.LB_MULTIPLE)
        species_label_peri = wx.StaticText(session_panel, -1, "Perinucleus\n Species: ")
        species_sizer_peri = wx.BoxSizer(wx.HORIZONTAL)
        species_sizer_peri.Add(species_label_peri)
        species_sizer_peri.Add(self.species_list_peri)
        species_sizer.Add(species_sizer_peri, border=7)

        self.species_list_mid = wx.CheckListBox(session_panel, -1, size=(200, -1), style=wx.LB_MULTIPLE)
        species_label_mid = wx.StaticText(session_panel, -1, "Cytoplasm\n Species: ")
        species_sizer_mid = wx.BoxSizer(wx.HORIZONTAL)
        species_sizer_mid.Add(species_label_mid)
        species_sizer_mid.Add(self.species_list_mid)
        species_sizer.Add(species_sizer_mid, border=7)

        self.species_list_api = wx.CheckListBox(session_panel, -1, size=(200, -1), style=wx.LB_MULTIPLE)
        species_label_api = wx.StaticText(session_panel, -1, "Cell Membrane\n Species: ")
        species_sizer_api = wx.BoxSizer(wx.HORIZONTAL)
        species_sizer_api.Add(species_label_api)
        species_sizer_api.Add(self.species_list_api)
        species_sizer.Add(species_sizer_api, border=7)

        panel_vbox.Add(species_sizer, flag=wx.ALIGN_CENTER | wx.TOP, border=7)

        btn_submit = wx.Button(session_panel, -1, "Lets Go!")
        panel_vbox.Add(btn_submit, flag=wx.ALIGN_CENTER | wx.TOP, border=7)
        btn_submit.Bind(wx.EVT_BUTTON, self.go)

        session_panel.SetSizer(panel_vbox)
        panel_vbox.Fit(session_panel)
        self.SetSize((self.world.dispW/1.3, self.world.dispH/2))
        self.Centre()

    def add_files(self, e):
        open_results_file(self)
        for key in self.world.results.keys():
            self.species_dict[key] = []
            for species in self.world.results[key].keys():
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

    def go(self, e):
        self.world.title = self.title_text.GetLineText(0)
        self.parse_species()
        self.Close()

    def parse_species(self):
        self.world.species_dict = {}
        inner = self.species_list_peri.GetCheckedStrings()[0]
        middle = self.species_list_mid.GetCheckedStrings()[0]
        outer = self.species_list_api.GetCheckedStrings()[0]
        loc_flag = 0
        for file_name in self.world.results.keys():
            for result in self.world.results[file_name].keys():
                if not result == "Time":
                    print result
                    print inner
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

                    if species not in self.world.species_dict.keys():
                        self.world.species_dict[species] = [(species,location,flag)]
                    else:
                        self.world.species_dict[species].append((species,location,flag))

padding = 5


class SessionWizard(wx.wizard.Wizard):

    def __init__(self, title, img_filename=""):
        wx.wizard.Wizard.__init__(self, None, -1, title)
        self.pages = []

    def add_page(self, page):
        if self.pages:
            previous_page = self.pages[-1]
            page.prev = previous_page
            previous_page.next = page
        self.pages.append(page)

    def run(self):
        self.RunWizard(self.pages[0])


class wizard_page(wizmod.PyWizardPage):

    def __init__(self, parent, title):
        wx.wizard.PyWizardPage.__init__(self, parent)
        self.next, self.prev = None
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        title = wx.StaticText(self, -1, title)
        title.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.sizer.AddWindow(title, 0, wx.ALIGN_LEFT|wx.ALL, padding)
        self.sizer.AddWindow(wx.StaticLine(self, -1), 0, wx.EXPAND|wx.ALL, padding)
        self.SetSizer(self.sizer)

    def add_widget(self, widget):
        self.sizer.Add(widget, 0, wx.EXPAND|wx.ALL, padding)

"""
if __name__ == '__main__':
    # Create wizard and add any kind pages you'd like
    session_starter = SessionWizard('Simple Wizard', img_filename='wiz.png')
    page1 = wizard_page(session_starter, 'Page 1')  # Create a first page
    page1.add_stuff(wx.StaticText(page1, -1, 'Hola'))
    session_starter.add_page(page1)

    # Add some more pages
    session_starter.add_page( wizard_page(session_starter, 'Page 2') )
    session_starter.add_page( wizard_page(session_starter, 'Page 3') )

    session_starter.run() # Show the main window

    # Cleanup
    session_starter.Destroy()
"""

