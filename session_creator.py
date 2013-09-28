import wx


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

        model_list = wx.ListBox(session_panel, -1, size=(300, -1), style=wx.LB_SINGLE)
        model_label = wx.StaticText(session_panel, -1, "Model: ")
        model_sizer = wx.BoxSizer(wx.HORIZONTAL)
        model_sizer.Add(model_label)
        model_sizer.Add(model_list)
        panel_vbox.Add(model_sizer, flag=wx.ALIGN_CENTER | wx.TOP, border=7)

        session_panel.SetSizer(panel_vbox)
        panel_vbox.Fit(session_panel)
        (dispW, dispH) = wx.DisplaySize()
        self.SetSize((dispW/2, dispH/2))
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

    def remove_files(self, e):
        self.chosen_paths = [path for i, path in enumerate(self.chosen_paths) if i not in self.file_list.GetSelections()]
        self.file_list.Clear()
        for path in self.chosen_paths:
            self.file_list.Append(path.split('/')[-1])
