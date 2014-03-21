import wx
from plot_dialog import Plot_Dialog
from custom_ui_elements import BioPepaCollapsiblePane
from utils import refresh_plot
from worldstate import WorldState

_HEIGHT = 20
_WIDTH = 20
_BG_COLOUR = 'white'


class Legend(object):

    def __init__(self, leg_panel):
        """
        self.legend_panel - where this is drawn
        """
        self.legend_panel = leg_panel
        #WorldState.Instance() = WorldState.Instance()

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
        font = wx.Font(28, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        title.SetFont(font)
        vbox_leg.Add(title, flag=wx.CENTER)

        #For each results file add a collapsible pane
        #for each species in the file add a 'line' into the collpane
        for result in WorldState.Instance().session_dict['lines']:
            collpane = BioPepaCollapsiblePane(self.legend_panel, result)
            vbox_leg.Add(collpane, 0, wx.GROW | wx.ALL, 5)

            collpane_body = collpane.GetPane()
            collpane_body.SetBackgroundColour(_BG_COLOUR)

            vbox_collpane = wx.BoxSizer(wx.VERTICAL)

            line1 = wx.StaticLine(collpane_body)
            vbox_collpane.Add(line1, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 10)

            for key in WorldState.Instance().session_dict['lines'][result]:
                hbox_collpane = wx.BoxSizer(wx.HORIZONTAL)

                vbox_coll = wx.BoxSizer(wx.VERTICAL)

                species_label = wx.StaticText(collpane_body, -1, key, style=wx.ALIGN_CENTRE)
                vbox_coll.Add(species_label, 0, wx.TOP|wx.BOTTOM, 5)

                btn_colour = wx.Button(collpane_body, -1, '', size=(_WIDTH, _HEIGHT))
                btn_colour.Disable()
                btn_colour.SetBackgroundColour(WorldState.Instance().session_dict['lines'][result][key].flat_colour)
                hbox_collpane.Add(btn_colour, 0, wx.ALL, 2)

                cb_show_hide = wx.CheckBox(collpane_body, -1, 'Show')
                hbox_collpane.Add(cb_show_hide, 0, wx.ALL, 2)
                cb_show_hide.SetValue(WorldState.Instance().session_dict['lines'][result][key].plot_line)
                cb_show_hide.Bind(wx.EVT_CHECKBOX, self.show_hide_click)

                cb_intense = wx.CheckBox(collpane_body, -1, 'Intense')
                hbox_collpane.Add(cb_intense, 0, wx.ALL, 2)
                cb_intense.SetValue(WorldState.Instance().session_dict['lines'][result][key].intense_plot)
                cb_intense.Bind(wx.EVT_CHECKBOX, self.intensity_click)

                btn_props = wx.Button(collpane_body, -1, 'Settings', size=(70, _HEIGHT))
                btn_props.Bind(wx.EVT_BUTTON, self.launch_dialog)
                hbox_collpane.Add(btn_props, 0, wx.ALL, 2)

                vbox_coll.Add(hbox_collpane, 0, wx.BOTTOM, 5)
                vbox_collpane.Add(vbox_coll)

                line2 = wx.StaticLine(collpane_body)
                vbox_collpane.Add(line2, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 10)

            collpane_body.SetSizer(vbox_collpane)
            vbox_collpane.Fit(collpane_body)

        self.legend_panel.SetSizer(vbox_leg)
        self.legend_panel.Layout()
        self.legend_panel.SetupScrolling()

        for child in self.legend_panel.GetChildren():
            try:
                child.Expand()
            except:
                pass

    def show_hide_click(self, event):
        """
        Updates the line to say don't or do draw
        """
        cb_show_hide = event.GetEventObject()
        file_key = cb_show_hide.GetParent().GetParent().GetLabel()
        species_key = self.get_species(cb_show_hide)
        WorldState.Instance().session_dict['lines'][file_key][species_key].plot_line = cb_show_hide.GetValue()
        WorldState.Instance().lamport_clock += 1
        WorldState.Instance().push_state()
        WorldState.Instance().reorder(WorldState.Instance().lamport_clock)
        refresh_plot()

    def intensity_click(self, event):
        """
        Event for toggling between colour intensity plot and normal plot
        """
        cb_intense = event.GetEventObject()
        file_key = cb_intense.GetParent().GetParent().GetLabel()
        species_key = self.get_species(cb_intense)
        WorldState.Instance().session_dict['lines'][file_key][species_key].intense_plot = cb_intense.GetValue()
        WorldState.Instance().lamport_clock += 1
        WorldState.Instance().push_state()
        WorldState.Instance().reorder(WorldState.Instance().lamport_clock)
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
        plot_prefs.set_line(WorldState.Instance().session_dict['lines'][file_key][species_key])
        plot_prefs.ShowModal()
        plot_prefs.Destroy()

        self.update(btn_props.GetParent(), file_key, species_key)

        #WorldState.Instance().push_state()
        #WorldState.Instance().reorder(WorldState.Instance().lamport_clock)

        WorldState.Instance().client.update_legend(WorldState.Instance().session_dict['lines'][file_key][species_key], file_key, species_key)

    def update(self, csv, file_key, species_key):
        """
        Updates the legend to reflect any new changes - colour, show/hide,
        intense/normal
        """
        update = False
        for child in csv.GetChildren():
            if (child.GetName() == "staticText"):
                update = True if (child.GetLabel() == species_key) else False

            if child.GetLabel() == "" and update:
                child.SetBackgroundColour(WorldState.Instance().session_dict['lines'][file_key][species_key].flat_colour)
            elif child.GetName() == "check" and update:
                if child.GetLabel() == "Show":
                    child.SetValue(WorldState.Instance().session_dict['lines'][file_key][species_key].plot_line)
                elif child.GetLabel() == "Ints" and update:
                    child.SetValue(WorldState.Instance().session_dict['lines'][file_key][species_key].intense_plot)
        self.legend_panel.Refresh()
        refresh_plot()
