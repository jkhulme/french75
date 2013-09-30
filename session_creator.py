import wx
from biopepa_csv_parser import BioPepaCsvParser


class SessionDialog(wx.Dialog):

    def __init__(self, *args, **kw):
        super(SessionDialog, self).__init__(*args, **kw)

        self.chosen_paths = []

        session_panel = wx.Panel(self)
        panel_vbox = wx.BoxSizer(wx.VERTICAL)

        title_text = wx.TextCtrl(session_panel, -1, size=(300, -1))
        title_label = wx.StaticText(session_panel, -1, "Title: ")
        title_sizer = wx.BoxSizer(wx.HORIZONTAL)
        title_sizer.Add(title_label)
        title_sizer.Add(title_text)
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
        species_label_mid = wx.StaticText(session_panel, -1, "No Man's Land\n Species: ")
        species_sizer_mid = wx.BoxSizer(wx.HORIZONTAL)
        species_sizer_mid.Add(species_label_mid)
        species_sizer_mid.Add(self.species_list_mid)
        species_sizer.Add(species_sizer_mid, border=7)


        self.species_list_api = wx.CheckListBox(session_panel, -1, size=(200, -1), style=wx.LB_MULTIPLE)
        species_label_api = wx.StaticText(session_panel, -1, "Apinucleus\n Species: ")
        species_sizer_api = wx.BoxSizer(wx.HORIZONTAL)
        species_sizer_api.Add(species_label_api)
        species_sizer_api.Add(self.species_list_api)
        species_sizer.Add(species_sizer_api, border=7)

        panel_vbox.Add(species_sizer, flag=wx.ALIGN_CENTER | wx.TOP, border=7)

        session_panel.SetSizer(panel_vbox)
        panel_vbox.Fit(session_panel)
        (dispW, dispH) = wx.DisplaySize()
        self.SetSize((dispW/1.3, dispH/2))
        self.Centre()

    def add_files(self, e):
        file_chooser = wx.FileDialog(
            self,
            message="Choose a file",
            wildcard="*.csv",
            style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR)
        if file_chooser.ShowModal() == wx.ID_OK:
            paths = file_chooser.GetPaths()
            for path in paths:
                self.chosen_paths.append(path)
                self.file_list.Append(path.split('/')[-1])
            file_chooser.Destroy()
        else:
            file_chooser.Destroy()

        results = {}
        parser = BioPepaCsvParser()
        for path in paths:
            parser.parse_csv(path)
            results[path.split('/')[-1]] = parser.results_dict
        keys = []
        for key in results.keys():
            for species in results[key].keys():
                if species != 'Time':
                    keys.append(species)
        for key in keys:
            self.species_list.Append(key)

    def remove_files(self, e):
        self.chosen_paths = [path for i, path in enumerate(self.chosen_paths) if i not in self.file_list.GetSelections()]
        self.file_list.Clear()
        for path in self.chosen_paths:
            self.file_list.Append(path.split('/')[-1])

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
