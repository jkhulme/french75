import wx
import wx.lib.agw.pycollapsiblepane as PCP
import platform


class Legend(object):

    """
    self.legend_panel - where this is drawn
    self.vbox_leg - sizer for the panel
    self.results - the data
    self.plotter - for redrawing the graph
    """

    def __init__(self, leg_panel):
        self.legend_panel = leg_panel
        self.vbox_leg = wx.BoxSizer(wx.VERTICAL)

    """
    Handles the legend, one collapsible pane for each file, one set of controls
    for each plot within that
    """
    def draw_legend(self, plotter, results):
        self.results = results
        self.plotter = plotter

        for child in self.legend_panel.GetChildren():
            child.Destroy()

        for result in self.results:
            if (platform.system() == "Linux"):
                collpane = PCP.PyCollapsiblePane(self.legend_panel, wx.ID_ANY, result)
            else:
                collpane = wx.CollapsiblePane(self.legend_panel, wx.ID_ANY, result)
            collpane.Expand()

            self.vbox_leg.Add(collpane, 0, wx.GROW | wx.ALL, 5)

            collpane_body = collpane.GetPane()
            vbox_collpane = wx.BoxSizer(wx.VERTICAL)

            for key in self.results[result]:
                cb_show_hide = wx.CheckBox(collpane_body, -1, key + '- Show', (10, 10))
                vbox_collpane.Add(cb_show_hide)
                cb_show_hide.SetValue(self.results[result][key].showhide)
                cb_show_hide.Bind(wx.EVT_CHECKBOX, self.show_hide_click)

                cb_intense = wx.CheckBox(collpane_body, -1, key + '- Intensity Plot', (10, 10))
                vbox_collpane.Add(cb_intense)
                cb_intense.SetValue(self.results[result][key].intense_plot)
                cb_intense.Bind(wx.EVT_CHECKBOX, self.intensity_click)

            collpane_body.SetSizer(vbox_collpane)
            vbox_collpane.SetSizeHints(collpane_body)

        self.legend_panel.SetSizer(self.vbox_leg)
        self.vbox_leg.Fit(self.legend_panel)

    """
    Event for showing/hiding the plot
    """
    def show_hide_click(self, event):
        cb_show_hide = event.GetEventObject()
        self.results[cb_show_hide.GetParent().GetParent().GetLabel()][cb_show_hide.GetLabel().split('-')[0].strip()].showhide = cb_show_hide.GetValue()
        self.plotter.draw_legend = False
        self.plotter.plot()

    """
    Event for toggling between colour intensity plot and normal plot
    """
    def intensity_click(self, event):
        cb_intense = event.GetEventObject()
        self.results[cb_intense.GetParent().GetParent().GetLabel()][cb_intense.GetLabel().split('-')[0].strip()].intense_plot = cb_intense.GetValue()
        self.plotter.draw_legend = False
        self.plotter.plot()
