import wx
from plot_dialog import Plot_Dialog
from custom_ui_elements import BioPepaCollapsiblePane
from utils import refresh_plot
from worldstate import WorldState

_HEIGHT = 20
_WIDTH = 45
_BG_COLOUR = 'white'


class Legend(object):

    def __init__(self, leg_panel):
        """
        self.legend_panel - where this is drawn
        """
        self.legend_panel = leg_panel
        self.world = WorldState.Instance()


    def draw_legend(self):
        """
        Handles the legend, one collapsible pane for each file, one set of
        controls for each plot within that
        """
        vbox_leg = wx.BoxSizer(wx.VERTICAL)

        #If we don't destroy them first they will just get redrawn everytime.
        for child in self.legend_panel.GetChildren():
            child.Destroy()

        title = wx.StaticText(self.legend_panel, wx.ID_ANY, 'Legend', style=wx.ALIGN_LEFT)
        font = wx.Font(14, wx.MODERN, wx.NORMAL, wx.BOLD)
        title.SetFont(font)
        vbox_leg.Add(title, flag=wx.CENTER)

        #For each results file add a collapsible pane
        #for each species in the file add a 'line' into the collpane
        for result in self.world.session_dict['lines']:
            collpane = BioPepaCollapsiblePane(self.legend_panel, result)
            vbox_leg.Add(collpane, 0, wx.GROW | wx.ALL, 5)
            collpane_body = collpane.GetPane()
            collpane_body.SetBackgroundColour(_BG_COLOUR)
            vbox_collpane = wx.BoxSizer(wx.VERTICAL)

            for key in self.world.session_dict['lines'][result]:
                hbox_collpane = wx.BoxSizer(wx.HORIZONTAL)
                vbox_coll = wx.BoxSizer(wx.VERTICAL)
                species_label = wx.StaticText(collpane_body, -1, key, style=wx.ALIGN_CENTRE)
                vbox_coll.Add(species_label)

                btn_colour = wx.Button(collpane_body, -1, '', size=(_WIDTH, _HEIGHT))
                btn_colour.Disable()
                btn_colour.SetBackgroundColour(self.world.session_dict['lines'][result][key].flat_colour)
                hbox_collpane.Add(btn_colour)

                cb_show_hide = wx.CheckBox(collpane_body, -1, 'Show')
                hbox_collpane.Add(cb_show_hide)
                cb_show_hide.SetValue(self.world.session_dict['lines'][result][key].plot_line)
                cb_show_hide.Bind(wx.EVT_CHECKBOX, self.show_hide_click)

                cb_intense = wx.CheckBox(collpane_body, -1, 'Ints')
                hbox_collpane.Add(cb_intense)
                cb_intense.SetValue(self.world.session_dict['lines'][result][key].intense_plot)
                cb_intense.Bind(wx.EVT_CHECKBOX, self.intensity_click)

                btn_props = wx.Button(collpane_body, -1, 'Prefs', size=(_WIDTH, _HEIGHT))
                btn_props.Bind(wx.EVT_BUTTON, self.launch_dialog)
                hbox_collpane.Add(btn_props)
                vbox_coll.Add(hbox_collpane)
                vbox_collpane.Add(vbox_coll)

            collpane_body.SetSizer(vbox_collpane)
            vbox_collpane.Fit(collpane_body)

        self.legend_panel.SetSizer(vbox_leg)
        self.legend_panel.Layout()
        #vbox_leg.Fit(self.legend_panel)
        self.legend_panel.SetupScrolling()

        for child in self.legend_panel.GetChildren():
            try:
                child.Expand()
            except:
                pass
    """
    Updates the line to say don't or do draw
    """
    def show_hide_click(self, event):
        cb_show_hide = event.GetEventObject()
        file_key = cb_show_hide.GetParent().GetParent().GetLabel()
        species_key = self.get_species(cb_show_hide)
        self.world.session_dict['lines'][file_key][species_key].plot_line = cb_show_hide.GetValue()
        self.world.push_state()
        refresh_plot()

    """
    Event for toggling between colour intensity plot and normal plot
    """
    def intensity_click(self, event):
        cb_intense = event.GetEventObject()
        file_key = cb_intense.GetParent().GetParent().GetLabel()
        species_key = self.get_species(cb_intense)
        self.world.session_dict['lines'][file_key][species_key].intense_plot = cb_intense.GetValue()
        self.world.push_state()
        refresh_plot()

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
        plot_prefs.set_line(self.world.session_dict['lines'][file_key][species_key])
        plot_prefs.ShowModal()
        plot_prefs.Destroy()
        self.update(btn_props.GetParent(), file_key, species_key)
        refresh_plot()

    def update(self, csv, file_key, species_key):
        """
        Updates the legend to reflect any new changes - colour, show/hide,
        intense/normal
        """
        for child in csv.GetChildren():
            if (child.GetName() == "staticText"):
                update = True if (child.GetLabel() == species_key) else False

            if child.GetLabel() == "" and update:
                child.SetBackgroundColour(self.world.session_dict['lines'][file_key][species_key].flat_colour)
            if child.GetName() == "check" and update:
                if child.GetLabel() == "S":
                    child.SetValue(self.world.session_dict['lines'][file_key][species_key].plot_line)
                if child.GetLabel() == "I" and update:
                    child.SetValue(self.world.session_dict['lines'][file_key][species_key].intense_plot)
        self.legend_panel.SetupScrolling()
        self.legend_panel.Refresh()
