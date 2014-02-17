import wx
import wx.lib.agw.pycollapsiblepane as PCP


class Test(wx.Frame):

    def cp(self):
        cp = wx.CollapsiblePane(self, wx.ID_ANY, label="Details:")
        frame_sizer = wx.BoxSizer(wx.VERTICAL)
        title = wx.StaticText(self, wx.ID_ANY, 'Legend')
        frame_sizer.Add(title)
        frame_sizer.Add(cp, 0, wx.GROW | wx.ALL, 5)
        cp_pane = cp.GetPane()
        cp_sizer = wx.BoxSizer(wx.VERTICAL)
        cb = wx.CheckBox(cp_pane, -1, "checkbox", (10, 10))
        cb.Bind(wx.EVT_CHECKBOX, self.OnClick)
        cp_sizer.Add(cb)
        cp_pane.SetSizer(cp_sizer)
        cp_sizer.SetSizeHints(cp_pane)
        cp.SetLabel("testlabel")
        self.SetSizer(frame_sizer)
        frame_sizer.Fit(self)


    def OnClick(self, event):
        check = event.GetEventObject()
        check_parent = check.GetParent().GetParent()

if __name__ == '__main__':
    app = wx.App()
    gui = Test(None)
    Test.cp(gui)
    gui.Show()
    app.MainLoop()
