"""
Used as template to get matplotlib plotting with wx backend.  Stripped down version of that guys web version that is public domain
"""

import wx
import matplotlib
matplotlib.use('WXAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigCanvas


class BarsFrame(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None)
        self.data = [5, 6, 9, 14]
        self.create_main_panel()
        self.draw_figure()

    def create_main_panel(self):
        self.panel = wx.Panel(self)
        self.fig = Figure((5.0, 4.0))
        self.canvas = FigCanvas(self.panel, -1, self.fig)
        self.axes = self.fig.add_subplot(111)
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.vbox.Add(self.canvas)
        self.panel.SetSizer(self.vbox)
        self.vbox.Fit(self)

    def draw_figure(self):
        x = range(len(self.data))
        self.axes.clear()
        self.axes.bar(left=x, height=self.data)
        self.canvas.draw()

    def on_exit(self, event):
        self.Destroy()

if __name__ == '__main__':
    app = wx.PySimpleApp()
    app.frame = BarsFrame()
    app.frame.Show()
    app.MainLoop()
