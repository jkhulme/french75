import wx
from bufferedcanvas import *


class TestCanvas(BufferedCanvas):

    def __init__(self,parent,ID=-1):
        BufferedCanvas.__init__(self,parent,ID)


    def draw(self, dc):
        print "drawing"
        dc.SetBackground(wx.Brush("Black"))
        dc.Clear()

        dc.SetBrush(wx.BLUE_BRUSH)
        dc.SetPen(wx.Pen('Red', 4))
        dc.DrawRectangle(20,20,300,200)


class TestFrame(wx.Frame):

    def __init__(self,
                 parent=None,
                 ID=-1,
                 title="BufferedCanvas Test",
                 pos=wx.DefaultPosition,
                 size=wx.DefaultSize,
                 style=wx.DEFAULT_FRAME_STYLE):
        wx.Frame.__init__(self,parent,ID,title,pos,size,style)
        self.canvas = TestCanvas(self)
        self.Bind(wx.EVT_CLOSE, self.onClose)

    def onClose(self,event):
        self.Show(False)
        self.Destroy()


def main():
    app = wx.PySimpleApp()
    frame = TestFrame()
    frame.Show(True)
    app.MainLoop()
    frame.canvas.OnPaint(None)

if __name__ == '__main__':
    main()
