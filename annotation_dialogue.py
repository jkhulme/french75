import wx
from worldstate import WorldState
from animation_annotation import AnimationAnnotation

_PADDING = 5


class AnnotationDialogue(wx.Dialog):

    """
    The plot preferences dialog, user can change things like colour and
    thickness
    """
    def __init__(self, *args, **kw):
        super(AnnotationDialogue, self).__init__(*args, **kw)
        self.world = WorldState.Instance()

        panel_vbox = wx.BoxSizer(wx.VERTICAL)

        annotation_label = wx.StaticText(self, -1, "Annotation Text:")
        panel_vbox.Add(annotation_label, 0, wx.EXPAND|wx.TOP|wx.LEFT, 5)

        self.text_ctrl = wx.TextCtrl(self, -1, style=wx.TE_MULTILINE, size=(self.world.dispW/6, self.world.dispH/8))
        panel_vbox.Add(self.text_ctrl, 0, wx.EXPAND|wx.ALL, 10)

        line1 = wx.StaticLine(self)
        panel_vbox.Add(line1, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 10)

        duration_label = wx.StaticText(self, -1, "Annotation Duration:")
        panel_vbox.Add(duration_label, 0, wx.EXPAND|wx.TOP|wx.LEFT, 5)

        time_hbox = wx.BoxSizer(wx.HORIZONTAL)

        start_vbox = wx.BoxSizer(wx.VERTICAL)
        start_label = wx.StaticText(self, -1, "Start:")
        start_vbox.Add(start_label)

        self.start_time = wx.SpinCtrl(self, max=1000000, size=(120, -1), initial=int(self.world.session_dict['clock']), value=str(int(self.world.session_dict['clock'])))
        self.start_time.Bind(wx.EVT_SPINCTRL, self.calculate_duration)
        start_vbox.Add(self.start_time, 0, wx.ALL, 5)

        time_hbox.Add(start_vbox)

        end_vbox = wx.BoxSizer(wx.VERTICAL)

        end_label = wx.StaticText(self, -1, "Finish:")
        end_vbox.Add(end_label)

        self.end_time = wx.SpinCtrl(self, max=1000000, size=(120, -1), initial=int(self.world.session_dict['clock'] + self.world.session_dict['clock_increment']*100), value=str(int(self.world.session_dict['clock'] + self.world.session_dict['clock_increment']*100)))
        self.end_time.Bind(wx.EVT_SPINCTRL, self.calculate_duration)
        end_vbox.Add(self.end_time, 0, wx.ALL, 5)

        time_hbox.Add(end_vbox)

        panel_vbox.Add(time_hbox, 0, wx.ALL, 5)

        self.total_duration_label = wx.StaticText(self, -1, "Duration: 0s")
        panel_vbox.Add(self.total_duration_label, 0, wx.EXPAND|wx.BOTTOM|wx.LEFT, 5)
        self.calculate_duration(None)

        line3 = wx.StaticLine(self)
        panel_vbox.Add(line3, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 10)

        panel_vbox.Add((0,0), 1, wx.EXPAND)

        line2 = wx.StaticLine(self)
        panel_vbox.Add(line2, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 10)

        btn_hbox = wx.BoxSizer(wx.HORIZONTAL)

        okButton = wx.Button(self, label='Ok')
        closeButton = wx.Button(self, label='Cancel')
        okButton.Bind(wx.EVT_BUTTON, self.on_ok)
        closeButton.Bind(wx.EVT_BUTTON, self.on_cancel)

        btn_hbox.Add(okButton, 0, wx.ALL, 5)
        btn_hbox.Add(closeButton, 0, wx.ALL, 5)

        panel_vbox.Add(btn_hbox, 0, wx.ALL|wx.ALIGN_CENTRE, 5)

        self.SetSizer(panel_vbox)
        panel_vbox.Fit(self)

        self.SetSize((self.world.dispW/4, self.world.dispH/2))
        self.Centre()

    def calculate_duration(self, e):
        duration = int((self.end_time.GetValue() - self.start_time.GetValue()) * self.world.session_dict['clock_increment'])
        self.total_duration_label.SetLabel("Duration: " + str(duration/10000) + "s")

    def on_ok(self, e):
        text = self.text_ctrl.GetValue()
        start = self.start_time.GetValue()
        finish = self.end_time.GetValue()

        self.world.temp_anime_annotation = AnimationAnnotation(text, start, finish, self.world.session_dict['cur_annotation_id'])

        self.Close()

    def on_cancel(self, e):
        self.world.temp_anime_annotation = None
        self.Close()
