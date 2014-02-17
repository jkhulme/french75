#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx

class step_1(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY)

        sizer = wx.BoxSizer(wx.VERTICAL)
        txtOne = wx.TextCtrl(self, wx.ID_ANY, "")

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(txtOne, 0, wx.ALL, 5)

        self.SetSizer(sizer)

class step_2(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY)

        sizer = wx.BoxSizer(wx.VERTICAL)
        txtOne = wx.TextCtrl(self, wx.ID_ANY, "")

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(txtOne, 0, wx.ALL, 5)

        self.SetSizer(sizer)

class main_frame(wx.Frame):
    """Main Frame holding the main panel."""
    def __init__(self,*args,**kwargs):
        wx.Frame.__init__(self,*args,**kwargs)
        p = wx.Panel(self)

        stp1 = step_1(p)
        stp2 = step_2(p)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(stp1, 0, border = 5)
        sizer.Add(stp2, 0, border = 5)
        p.SetSizerAndFit(sizer)
        self.Show()

if __name__ == "__main__":
    app = wx.App(False)
    frame = main_frame(None,-1,size = (400,300))
    app.MainLoop()
