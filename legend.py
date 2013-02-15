import wx
import wx.lib.agw.pycollapsiblepane as PCP
import platform


class Legend(object):

    """
    self.legend_panel
    self.vbox_leg
    """
    def __init__(self, leg_panel):
        self.legend_panel = leg_panel

        self.vbox_leg = wx.BoxSizer(wx.VERTICAL)

    def draw_legend(self, plotter, results):
        self.results = results
        self.plotter = plotter
        for child in self.legend_panel.GetChildren():
            child.Destroy()
        for result in results:
            if (platform.system() == "Linux"):
                collpane = PCP.PyCollapsiblePane(self.legend_panel, wx.ID_ANY, result)
            else:
                collpane = wx.CollapsiblePane(self.legend_panel, wx.ID_ANY, result)
            collpane.Expand()

            self.vbox_leg.Add(collpane, 0, wx.GROW | wx.ALL, 5)
            win = collpane.GetPane()
            paneSz = wx.BoxSizer(wx.VERTICAL)
            for key in results[result]:
                cb = wx.CheckBox(win, -1, key, (10, 10))
                paneSz.Add(cb)
                cb.SetValue(results[result][key].showhide)
                cb.Bind(wx.EVT_CHECKBOX, self.OnClick)
                
                cb2 = wx.CheckBox(win, -1, key, (10, 10))
                paneSz.Add(cb2)
                cb2.SetValue(results[result][key].normal_plot)
                cb2.Bind(wx.EVT_CHECKBOX, self.OnClickTwo)
                
                label = wx.StaticText(win, -1, key)
                paneSz.Add(label)
            win.SetSizer(paneSz)
            paneSz.SetSizeHints(win)

        self.legend_panel.SetSizer(self.vbox_leg)
        self.vbox_leg.Fit(self.legend_panel)

    def OnClick(self, event):
        cb = event.GetEventObject()
        self.results[cb.GetParent().GetParent().GetLabel()][cb.GetLabel()].showhide = cb.GetValue()
        self.plotter.plot(False)

    def OnClickTwo(self, event):
        cb2 = event.GetEventObject()
        self.results[cb2.GetParent().GetParent().GetLabel()][cb2.GetLabel()].normal_plot = cb2.GetValue()
        self.plotter.plot(False)
