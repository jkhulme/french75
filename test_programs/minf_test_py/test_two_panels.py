#!/usr/bin/python

# helpwindow.py

import wx
import wx.html as html


class HelpWindow(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(HelpWindow, self).__init__(*args, **kwargs)

        self.splitter = wx.SplitterWindow(self, -1)
        self.panelLeft = wx.Panel(self.splitter, -1)

        self.panelRight = wx.Panel(self.splitter, -1)
        vbox2 = wx.BoxSizer(wx.VERTICAL)
        header = wx.Panel(self.panelRight, -1, size=(-1, 20))
        header.SetBackgroundColour('#6f6a59')
        header.SetForegroundColour('WHITE')
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        st = wx.StaticText(header, -1, 'Help', (5, 5))
        st2 = wx.StaticText(header, -1, 'Help', (5, 5))
        st3 = wx.StaticText(header, -1, 'Help', (5, 5))
        st4 = wx.StaticText(header, -1, 'Help', (5, 5))
        st5 = wx.StaticText(header, -1, 'Help', (5, 5))
        st6 = wx.StaticText(header, -1, 'Help', (5, 5))
        st7 = wx.StaticText(header, -1, 'Help', (5, 5))
        font = st.GetFont()
        font.SetPointSize(9)
        st.SetFont(font)
        hbox.Add(st, 1, wx.TOP | wx.BOTTOM | wx.LEFT, 5)

        header.SetSizer(hbox)

        vbox2.Add(st, 1, wx.EXPAND)
        vbox2.Add(st2, 1, wx.EXPAND)
        vbox2.Add(st3, 1, wx.EXPAND)
        vbox2.Add(st4, 1, wx.EXPAND)
        vbox2.Add(st5, 1, wx.EXPAND)
        vbox2.Add(st6, 1, wx.EXPAND)
        vbox2.Add(st7, 1, wx.EXPAND)

        help = html.HtmlWindow(self.panelRight, -1, style=wx.NO_BORDER)
        help.LoadPage('help.html')
        vbox2.Add(help, 1, wx.EXPAND)
        self.panelRight.SetSizer(vbox2)
        self.panelLeft.SetFocus()

        self.splitter.SplitVertically(self.panelLeft, self.panelRight)

        self.Centre()
        self.Show(True)

    def OnClose(self, event):
        self.Close()

    def OnHelp(self, event):
        self.splitter.SplitVertically(self.panelLeft, self.panelRight)
        self.panelLeft.SetFocus()

    def CloseHelp(self, event):
        self.splitter.Unsplit()
        self.panelLeft.SetFocus()

    def OnKeyPressed(self, event):
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_F1:
            self.splitter.SplitVertically(self.panelLeft, self.panelRight)
            self.panelLeft.SetFocus()


app = wx.App()
HelpWindow(None)
app.MainLoop()
