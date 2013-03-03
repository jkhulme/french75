import wx


class Plot_Dialog(wx.Dialog):

    def __init__(self, *args, **kw):
        super(Plot_Dialog, self).__init__(*args, **kw)
        self.InitUI()
        self.SetSize((250, 200))

    def InitUI(self):

        dialog_panel = wx.Panel(self)
        panel_vbox = wx.BoxSizer(wx.VERTICAL)

        sb = wx.StaticBox(dialog_panel, label='Colors')
        sbs = wx.StaticBoxSizer(sb, orient=wx.VERTICAL)
        self.cb_show_hide = wx.CheckBox(dialog_panel, -1, 'Show', (10, 10))
        sbs.Add(self.cb_show_hide)
        self.cb_intense = wx.CheckBox(dialog_panel, -1, 'Intensity Plot',
                                     (10, 10))
        sbs.Add(self.cb_intense)
        self.colour_picker = wx.ColourPickerCtrl(dialog_panel, -1)
        sbs.Add(self.colour_picker)

        dialog_panel.SetSizer(sbs)

        btn_hbox = wx.BoxSizer(wx.HORIZONTAL)
        okButton = wx.Button(self, label='Ok')
        closeButton = wx.Button(self, label='Cancel')
        btn_hbox.Add(okButton)
        btn_hbox.Add(closeButton, flag=wx.LEFT, border=5)

        panel_vbox.Add(dialog_panel, proportion=1, flag=wx.ALL |
                       wx.EXPAND, border=5)
        panel_vbox.Add(btn_hbox, flag=wx.ALIGN_CENTER | wx.TOP |
                       wx.BOTTOM, border=10)

        self.SetSizer(panel_vbox)

        okButton.Bind(wx.EVT_BUTTON, self.on_ok)
        closeButton.Bind(wx.EVT_BUTTON, self.on_cancel)

    def set_line(self, line):
        self.line = line
        self.cb_show_hide.SetValue(self.line.showhide)
        self.cb_intense.SetValue(self.line.intense_plot)
        self.colour_picker.SetColour(self.line.flat_colour)

    def rgb_to_hex(self, rgb):
        return '#%02x%02x%02x' % rgb

    def on_ok(self, e):
        self.line.showhide = self.cb_show_hide.GetValue()
        self.line.intense_plot = self.cb_intense.GetValue()
        rgb = (self.colour_picker.GetColour()[0], self.colour_picker.GetColour()[1], self.colour_picker.GetColour()[2])
        self.line.flat_colour = self.rgb_to_hex(rgb)
        self.Close()

    def on_cancel(self, e):
        self.Close()
