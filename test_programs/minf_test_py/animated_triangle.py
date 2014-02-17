import wx
import Vector2D


class SimpleGraphics(wx.Panel):
    def __init__(self, parent, size=(50, 50)):
        super(SimpleGraphics, self).__init__(parent,
                                     size=size,
                                     style=wx.NO_BORDER)

        self.color = "Black"
        self.thickness = 2
        self.pen = wx.Pen(self.color, self.thickness, wx.SOLID)
        self.MARGIN = 1 #px
        self.points = [[0.0, 0.5], [0.5, 0.0], [-0.5, -0.5]]
        self.pos = (0, 0)
        self.cur_vector = Vector2D(1, 1)

        self.InitBuffer()
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_IDLE, self.OnIdle)
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyArrow)
        # MOUSE TRACKING
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_MOTION, self.OnMotion)

        self.Bind(wx.EVT_PAINT, self.OnPaint)


    def InitBuffer(self):
        self.client_size = self.GetClientSize()
        self.buffer = wx.EmptyBitmap(self.client_size.width, self.client_size.height)
        dc = wx.BufferedDC(None, self.buffer)
        dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        dc.Clear()
        self.DrawImage(dc)
        self.reInitBuffer = False

    def OnSize(self, event):
        self.reInitBuffer = True

    def repaint_the_view(self):
        self.InitBuffer()
        self.Refresh()

    def OnIdle(self, event):
        if self.reInitBuffer:
            self.repaint_the_view()

    def OnKeyArrow(self, event):
        key_code = event.GetKeyCode()
        if key_code == wx.WXK_LEFT:
            self.rotate_points(degrees_to_rad(5))
        elif key_code == wx.WXK_RIGHT:
            self.rotate_points(degrees_to_rad(-5))
        self.repaint_the_view()
        event.Skip()

    def OnLeftDown(self, event):
        # get the mouse position and capture the mouse
        self.pos = event.GetPositionTuple()
        self.cur_vector = create_vector2d(self.pos[0], self.pos[1],
                                         self.client_size.width / 2,
                                         self.client_size.height / 2)
        self.CaptureMouse()

    def OnLeftUp(self, event):
        #release the mouse
        if self.HasCapture():
            self.ReleaseMouse()

    def OnMotion(self, event):
        if event.Dragging() and event.LeftIsDown():
            newPos = event.GetPositionTuple()
            new_vector = create_vector2d(newPos[0], newPos[1],
                                         self.client_size.width / 2,
                                         self.client_size.height / 2)
            if new_vector.lenth() > 0.00001:
                c = cos_a(self.cur_vector, new_vector)
                s = sin_a(self.cur_vector, new_vector)
                rot_matr = rotation_matrix(s, c)
                self.rotate_points(rot_matr=rot_matr)
                dc = wx.BufferedDC(wx.ClientDC(self), self.buffer) # this line I've added after posting the question
                self.repaint_the_view()
                self.cur_vector = new_vector
        event.Skip()

    def OnPaint(self, event):
        wx.BufferedPaintDC(self, self.buffer)

    def DrawImage(self, dc):
        dc.SetPen(self.pen)
        new_points = self.convetr_points_to_virtual()
        dc.DrawPolygon([wx.Point(x, y) for (x, y) in new_points])

    def to_x(self, X_Log):
        X_Window = self.MARGIN + (1.0 / 2) * (X_Log + 1) * (self.client_size.width - 2 * self.MARGIN)
        return int(X_Window)

    def to_y(self, Y_Log):
        Y_Window = self.MARGIN + (-1.0 / 2) * (Y_Log - 1) * (self.client_size.height - 2 * self.MARGIN)
        return int(Y_Window)

    def convetr_points_to_virtual(self):
        return [(self.to_x(x), self.to_y(y)) for (x, y) in self.points]

    def rotate_points(self, angle_in_degrees=None, rot_matr=None):
        if angle_in_degrees is None:
            self.points = [rotate_point(x, y , rotator_matrix=rot_matr) for (x, y) in self.points]
        else:
            self.points = [rotate_point(x, y , angle_in_degrees) for (x, y) in self.points]

class SimpleGraphicsFrame(wx.Frame):
    def __init__(self, parent, *args, **kwargs):
        wx.Frame.__init__(self, parent, *args, **kwargs)

        # Attributes
        self.panel = SimpleGraphics(self)

        # Layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.panel, 1, wx.EXPAND)
        self.SetSizer(sizer)

class SimpleGraphApp(wx.App):
    def OnInit(self):
        self.frame = SimpleGraphicsFrame(None,
                                 title="Drawing Shapes",
                                 size=(300, 400))
        self.frame.Show()
        return True

if __name__ == '__main__':
    app = SimpleGraphApp(False)
    app.MainLoop()
