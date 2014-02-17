#!/usr/bin/python

# operations.py

import wx
import time
from threading import Thread

class Operations(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(270, 220))
        self.count = 0
        self.animation_panel = wx.Panel(self,-1)
        self.animation_panel.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Centre()
        self.animation_panel.Parent.Refresh()
        t = Thread(target=self.animate, args=(1,))
        t.start()


    def OnPaint(self, event):
        print self.count
        self.count += 1
        self.dc = wx.PaintDC(self.animation_panel)
        self.dc.DrawArc(175, 100, 100, 75, 100, 100)
        self.dc.DrawArc(150, 100, 100, 50, 100, 100)
        self.dc.DrawArc(125, 100, 100, 25, 100, 100)

    def animate(self, n):
        while True:
            self.Refresh()
            time.sleep(n)

app = wx.App()
Operations(None, -1, 'Operations')
app.MainLoop()
