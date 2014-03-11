import wx
from utils import rgb_to_hex
from worldstate import WorldState


class Plot_Dialog(wx.Dialog):

    """
    The plot preferences dialog, user can change things like colour and
    thickness
    """

    def __init__(self, *args, **kw):
        super(Plot_Dialog, self).__init__(*args, **kw)
        self.world = WorldState.Instance()

        panel_vbox = wx.BoxSizer(wx.VERTICAL)

        preferences_label = wx.StaticText(self, -1, "Line Preferences:")
        panel_vbox.Add(preferences_label, 0, wx.EXPAND|wx.TOP|wx.LEFT|wx.BOTTOM, 10)

        line1 = wx.StaticLine(self)
        panel_vbox.Add(line1, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 10)

        self.cb_show_hide = wx.CheckBox(self, -1, 'Show Line', (10, 10), style=wx.ALIGN_RIGHT)
        panel_vbox.Add(self.cb_show_hide, 0, wx.EXPAND|wx.TOP|wx.LEFT, 10)

        self.cb_intense = wx.CheckBox(self, -1, 'Plot Intensity Gradient',
                                     (10, 10), style=wx.ALIGN_RIGHT)
        panel_vbox.Add(self.cb_intense, 0, wx.EXPAND|wx.TOP|wx.LEFT|wx.BOTTOM, 10)

        line2 = wx.StaticLine(self)
        panel_vbox.Add(line2, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 10)

        colour_hbox = wx.BoxSizer(wx.HORIZONTAL)

        colour_label = wx.StaticText(self, -1, "Line Colour:")
        colour_hbox.Add(colour_label)

        self.colour_picker = wx.ColourPickerCtrl(self, -1)
        colour_hbox.Add(self.colour_picker)

        panel_vbox.Add(colour_hbox, 0, wx.EXPAND|wx.TOP|wx.LEFT, 10)

        thickness_hbox = wx.BoxSizer(wx.HORIZONTAL)

        thickness_label = wx.StaticText(self, -1, "Line Thickness")
        thickness_hbox.Add(thickness_label)

        self.thick_spin = wx.SpinCtrl(self, -1, "2")
        thickness_hbox.Add(self.thick_spin)

        panel_vbox.Add(thickness_hbox, 0, wx.EXPAND|wx.TOP|wx.LEFT|wx.BOTTOM, 10)

        line4 = wx.StaticLine(self)
        panel_vbox.Add(line4, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 10)
        panel_vbox.Add((0,0), 1, wx.EXPAND)
        line5 = wx.StaticLine(self)
        panel_vbox.Add(line5, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 10)

        btn_hbox = wx.BoxSizer(wx.HORIZONTAL)

        okButton = wx.Button(self, label='Ok')
        closeButton = wx.Button(self, label='Cancel')
        okButton.Bind(wx.EVT_BUTTON, self.on_ok)
        closeButton.Bind(wx.EVT_BUTTON, self.on_cancel)
        btn_hbox.Add(okButton)
        btn_hbox.Add(closeButton, flag=wx.LEFT, border=10)

        panel_vbox.Add(btn_hbox, flag=wx.ALIGN_CENTER | wx.TOP |
                       wx.BOTTOM, border=10)

        self.SetSizer(panel_vbox)
        panel_vbox.Fit(self)
        self.SetSize((self.world.dispW/4, self.world.dispH/2))

        self.Centre()

    def set_line(self, line):
        """
        Set dialog ui elements to values from line
        """
        self.line = line
        self.cb_show_hide.SetValue(self.line.plot_line)
        self.cb_intense.SetValue(self.line.intense_plot)
        self.colour_picker.SetColour(self.line.flat_colour)
        self.thick_spin.SetValue(self.line.thickness)

    def on_ok(self, e):
        """
        Update the line to values from ui elements
        """
        self.line.plot_line = self.cb_show_hide.GetValue()
        self.line.intense_plot = self.cb_intense.GetValue()
        self.line.thickness = self.thick_spin.GetValue()
        try:
            (r, g, b) = self.colour_picker.GetColour().Get()
            self.line.rgb_tuple = (r, g, b)
            self.line.flat_colour = rgb_to_hex((r, g, b))
            self.line.sub_plot_tuples = self.line.plot_sub_plots(self.line.interpolated_results, self.line.interval)
            self.line.normalise()
        except:
            print "No colour change"
        self.world.lamport_clock += 1
        self.world.push_state()
        self.world.reorder(self.world.lamport_clock)
        self.Close()

    def on_cancel(self, e):
        self.Close()
