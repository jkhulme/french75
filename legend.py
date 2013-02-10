import wx


class Legend():

    """
    self.legend_panel
    self.vbox_leg
    """
    def __init__(self, leg_panel):
        self.legend_panel = leg_panel

        self.vbox_leg = wx.BoxSizer(wx.VERTICAL)

    def draw_legend(self, files):
        for child in self.legend_panel.GetChildren():
            child.Destroy()
        for name in files:
            collpane = wx.CollapsiblePane(self.legend_panel, wx.ID_ANY, name)
            #collpane2 = wx.CollapsiblePane(self.legend_panel, wx.ID_ANY, "Betails:")

            # add the pane with a zero proportion value to the 'sz' sizer which contains it
            self.vbox_leg.Add(collpane, 0, wx.GROW | wx.ALL, 5)
            #self.vbox_leg.Add(collpane2, 0, wx.GROW | wx.ALL, 5)

            win = collpane.GetPane()
            paneSz = wx.BoxSizer(wx.VERTICAL)
            paneSz.Add(wx.StaticText(win, wx.ID_ANY, "test!"), 1, wx.GROW | wx.ALL, 2)
            win.SetSizer(paneSz)
            paneSz.SetSizeHints(win)

        self.legend_panel.SetSizer(self.vbox_leg)
        self.vbox_leg.Fit(self.legend_panel)
