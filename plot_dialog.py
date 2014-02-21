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

        #Should this be tied more to real units?
        self.thick_spin = wx.SpinCtrl(dialog_panel, -1, "2")
        sbs.Add(self.thick_spin)

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

        self.SetSize((self.world.dispW/4, self.world.dispH/2))
        self.Centre()

    """
    Set dialog ui elements to values from line
    """
    def set_line(self, line):
        self.line = line
        self.cb_show_hide.SetValue(self.line.plot_line)
        self.cb_intense.SetValue(self.line.intense_plot)
        self.colour_picker.SetColour(self.line.flat_colour)
        self.thick_spin.SetValue(self.line.thickness)

    """
    Update the line to values from ui elements
    """
    def on_ok(self, e):
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
        self.world.push_state()
        self.Close()

    def on_cancel(self, e):
        self.Close()
