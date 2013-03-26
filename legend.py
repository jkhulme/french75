import wx
import wx.lib.agw.pycollapsiblepane as PCP
import platform
from plot_dialog import Plot_Dialog


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

        title = wx.StaticText(self.legend_panel, wx.ID_ANY, 'Legend', style=wx.ALIGN_CENTER)
        font = wx.Font(14, wx.MODERN, wx.NORMAL, wx.BOLD)
        title.SetFont(font)
        self.vbox_leg.Add(title, flag=wx.CENTER)

        for result in self.results:
            if (platform.system() == "Linux"):
                collpane = PCP.PyCollapsiblePane(self.legend_panel, wx.ID_ANY, result)
            else:
                collpane = wx.CollapsiblePane(self.legend_panel, wx.ID_ANY, result)

            self.vbox_leg.Add(collpane, 0, wx.GROW | wx.ALL, 5)

            collpane_body = collpane.GetPane()
            collpane_body.SetBackgroundColour('white')
            self.vbox_collpane = wx.BoxSizer(wx.VERTICAL)

            for key in self.results[result]:
                hbox_collpane = wx.BoxSizer(wx.HORIZONTAL)
                vbox_coll = wx.BoxSizer(wx.VERTICAL)
                species_label = wx.StaticText(collpane_body, -1, key, style=wx.ALIGN_CENTRE)
                vbox_coll.Add(species_label)

                btn_colour = wx.Button(collpane_body, -1, '', size=(20, 20))
                btn_colour.Disable()
                btn_colour.SetBackgroundColour(self.results[result][key].flat_colour)
                hbox_collpane.Add(btn_colour)

                cb_show_hide = wx.CheckBox(collpane_body, -1, 'S')
                hbox_collpane.Add(cb_show_hide)
                cb_show_hide.SetValue(self.results[result][key].showhide)
                cb_show_hide.Bind(wx.EVT_CHECKBOX, self.show_hide_click)

                cb_intense = wx.CheckBox(collpane_body, -1, 'I')
                hbox_collpane.Add(cb_intense)
                cb_intense.SetValue(self.results[result][key].intense_plot)
                cb_intense.Bind(wx.EVT_CHECKBOX, self.intensity_click)

                btn_props = wx.Button(collpane_body, -1, 'P', size=(20, 20))
                btn_props.Bind(wx.EVT_BUTTON, self.launch_dialog)
                hbox_collpane.Add(btn_props)
                vbox_coll.Add(hbox_collpane)
                self.vbox_collpane.Add(vbox_coll)

            collpane_body.SetSizer(self.vbox_collpane)
            self.vbox_collpane.Fit(collpane_body)

        self.legend_panel.SetSizer(self.vbox_leg)
        self.vbox_leg.Fit(self.legend_panel)

        for child in self.legend_panel.GetChildren():
            try:
                child.Expand()
            except:
                print "can't expand"

    """
    Event for showing/hiding the plot
    """
    def show_hide_click(self, event):
        cb_show_hide = event.GetEventObject()
        file_key = cb_show_hide.GetParent().GetParent().GetLabel()
        species_key = self.get_species(cb_show_hide)
        self.results[file_key][species_key].showhide = cb_show_hide.GetValue()
        self.plotter.draw_legend = False
        self.plotter.plot()

    """
    Event for toggling between colour intensity plot and normal plot
    """
    def intensity_click(self, event):
        cb_intense = event.GetEventObject()
        file_key = cb_intense.GetParent().GetParent().GetLabel()
        species_key = self.get_species(cb_intense)
        self.results[file_key][species_key].intense_plot = cb_intense.GetValue()
        self.plotter.draw_legend = False
        self.plotter.plot()

    def get_species(self, cb):
        for child in cb.GetParent().GetChildren():
            if (child.GetName() == "staticText"):
                species_key = child.GetLabel()
            if (child == cb):
                return species_key

    def launch_dialog(self, event):
        btn_props = event.GetEventObject()
        file_key = btn_props.GetParent().GetParent().GetLabel()
        species_key = self.get_species(btn_props)
        plot_prefs = Plot_Dialog(None, title='Change Plot Style')
        plot_prefs.set_line(self.results[file_key][species_key])
        plot_prefs.ShowModal()
        plot_prefs.Destroy()
        self.update(btn_props.GetParent(), file_key, species_key)
        self.plotter.draw_legend = False
        self.plotter.plot()

    def update(self, csv, file_key, species_key):
        print len(csv.GetChildren())
        update = False
        for child in csv.GetChildren():
            if (child.GetName() == "staticText"):
                if (child.GetLabel() == species_key):
                    update = True
                else:
                    update = False

            if child.GetLabel() == "" and update:
                child.SetBackgroundColour(self.results[file_key][species_key].flat_colour)
                print "changed colour"
            if child.GetName() == "check" and update:
                print "da fuck"
                if child.GetLabel() == "S":
                    child.SetValue(self.results[file_key][species_key].showhide)
                if child.GetLabel() == "I" and update:
                    print "int plot"
                    child.SetValue(self.results[file_key][species_key].intense_plot)
