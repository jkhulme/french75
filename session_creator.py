import wx

class SessionDialog(wx.Dialog):

    def __init__(self, *args, **kw):
        super(SessionDialog, self).__init__(*args, **kw)

        session_panel = wx.Panel(self)
        panel_vbox = wx.BoxSizer(wx.VERTICAL)

        title_text = wx.TextCtrl(session_panel, -1, size=(300, -1))
        title_label = wx.StaticText(session_panel, -1, "Title: ")
        title_sizer = wx.BoxSizer(wx.HORIZONTAL)
        title_sizer.Add(title_label)
        title_sizer.Add(title_text)
        panel_vbox.Add(title_sizer, flag=wx.ALIGN_CENTER | wx.TOP, border=7)

        file_list = wx.ListBox(session_panel, -1, size=(300, -1))
        file_label = wx.StaticText(session_panel, -1, "Results: ")
        file_sizer = wx.BoxSizer(wx.HORIZONTAL)
        file_sizer.Add(file_label)
        file_sizer.Add(file_list)
        panel_vbox.Add(file_sizer, flag=wx.ALIGN_CENTER | wx.TOP, border=7)

        file_toolbar = wx.BoxSizer(wx.HORIZONTAL)
        btn_add_file = wx.Button(session_panel, -1, "Add")
        btn_rem_file = wx.Button(session_panel, -1, "Remove")
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
