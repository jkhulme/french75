import wx


class Legend():

    """
    self.legend_panel
    self.vbox_leg
    """
    def __init__(self, leg_panel):
        self.legend_panel = leg_panel

        self.vbox_leg = wx.BoxSizer(wx.VERTICAL)

    def draw_legend(self, results):
        for child in self.legend_panel.GetChildren():
            child.Destroy()
        for result in results:
            collpane = wx.CollapsiblePane(self.legend_panel, wx.ID_ANY, result)

            self.vbox_leg.Add(collpane, 0, wx.GROW | wx.ALL, 5)
            win = collpane.GetPane()
            paneSz = wx.BoxSizer(wx.VERTICAL)
            for key in results[result]:
                self.cb = wx.CheckBox(win, -1, 'Show Title', (10, 10))
                paneSz.Add(self.cb)
                self.cb.SetValue(True)
                self.cb.Bind(wx.EVT_CHECKBOX,
                    lambda event: self.OnClick(event, 'somevalue'), self.cb)
                #wx.EVT_CHECKBOX(self.cb,
                #    self.cb.GetId(), self.getOnCheck(results[result][key]))
                paneSz.Add(wx.StaticText(win, wx.ID_ANY, key), 1, wx.GROW |
                    wx.ALL, 2)
            win.SetSizer(paneSz)
            paneSz.SetSizeHints(win)

        self.legend_panel.SetSizer(self.vbox_leg)
        self.vbox_leg.Fit(self.legend_panel)

    def OnClick(self, event, somearg):
        print somearg
