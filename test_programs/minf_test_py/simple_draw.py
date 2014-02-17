# draw lines, a rounded-rectangle and a circle on a wx.PaintDC() surface
# tested with Python24 and wxPython26     vegaseat      06mar2007
import wx


class MyFrame(wx.Frame):
    """a frame with a panel"""
    def __init__(self, parent=None, id=-1, title=None):
        wx.Frame.__init__(self, parent, id, title)
        self.panel = wx.Panel(self, size=(350, 200))
        self.panel.Bind(wx.EVT_PAINT, self.on_paint)
        self.Fit()

    def on_paint(self, event):
        # establish the painting surface
        dc = wx.PaintDC(self.panel)
        dc.SetPen(wx.Pen('blue', 4))
        # draw a blue line (thickness = 4)
        dc.DrawLine(50, 20, 300, 20)
        dc.SetPen(wx.Pen('red', 1))
        # draw a red rounded-rectangle
        rect = wx.Rect(50, 50, 100, 100)
        dc.DrawRoundedRectangleRect(rect, 8)
        # draw a red circle with yellow fill
        dc.SetBrush(wx.Brush('yellow'))
        x = 250
        y = 100
        r = 50
        dc.DrawCircle(x, y, r)
# test it ...
app = wx.App()
frame1 = MyFrame(title='rounded-rectangle & circle')
frame1.Center()
frame1.Show()
app.MainLoop()
