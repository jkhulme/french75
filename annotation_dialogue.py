import wx
from worldstate import WorldState

_PADDING = 5


class AnnotationDialogue(wx.Dialog):

    """
    The plot preferences dialog, user can change things like colour and
    thickness
    """
    def __init__(self, *args, **kw):
        wx.USER_TICMEPICKCTRL = 1
        super(AnnotationDialogue, self).__init__(*args, **kw)

        self.world = WorldState.Instance()
        #dialog_panel = wx.Panel(self)
        panel_vbox = wx.BoxSizer(wx.VERTICAL)

        self.text_ctrl = wx.TextCtrl(self, -1, style=wx.TE_MULTILINE, size=(self.world.session_dict['dispW']/6, self.world.session_dict['dispH']/8))
        panel_vbox.Add(self.text_ctrl, 0, wx.EXPAND|wx.ALL, 10)

        time_hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.start_time = wx.SpinCtrl(self, size=(120, -1))
        time_hbox.Add(self.start_time, 0, wx.ALL, 5)

        self.end_time = wx.SpinCtrl(self, size=(120, -1))
        time_hbox.Add(self.end_time, 0, wx.ALL, 5)
        panel_vbox.Add(time_hbox, 0, wx.ALL|wx.ALIGN_CENTRE, 5)

        btn_hbox = wx.BoxSizer(wx.HORIZONTAL)
        okButton = wx.Button(self, label='Ok')
        closeButton = wx.Button(self, label='Cancel')
        btn_hbox.Add(okButton, 0, wx.ALL, 5)
        btn_hbox.Add(closeButton, 0, wx.ALL, 5)
        panel_vbox.Add(btn_hbox, 0, wx.ALL|wx.ALIGN_CENTRE, 5)
        #btn_hbox.Fit(self)

        okButton.Bind(wx.EVT_BUTTON, self.on_ok)
        closeButton.Bind(wx.EVT_BUTTON, self.on_cancel)

        self.SetSizer(panel_vbox)
        panel_vbox.Fit(self)
        self.SetSize((self.world.session_dict['dispW']/4, self.world.session_dict['dispH']/2))

        #self.Layout()
        self.Centre()


    def on_ok(self, e):
        pass
        self.Close()

    def on_cancel(self, e):
        self.Close()
