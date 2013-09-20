import wx
from worldstate import WorldState


class CellSegment(object):

    def __init__(self, (tl_x, tl_y), radius, dc):
        self.world = WorldState.Instance()
        self.dc = dc
        self.centre_x, self.centre_y = tl_x, tl_y + radius

        self.outer_x1, self.outer_y1 = tl_x + radius, self.centre_y
        self.outer_x2, self.outer_y2 = tl_x, tl_y

        self.middle_x1, self.middle_y1 = tl_x + 2*(radius/3), self.centre_y
        self.middle_x2, self.middle_y2 = tl_x, tl_y + (radius/3)

        self.inner_x1, self.inner_y1 = tl_x + (radius/3), self.centre_y
        self.inner_x2, self.inner_y2 = tl_x, tl_y + 2*(radius/3)

        self.outer_brush_colour = 'red'
        self.middle_brush_colour = 'blue'
        self.inner_brush_colour = 'green'

    def paint(self):
        self.dc.SetBrush(wx.Brush(self.outer_brush_colour))
        self.dc.DrawArc(self.outer_x1, self.outer_y1, self.outer_x2, self.outer_y2, self.centre_x, self.centre_y)
        self.dc.SetBrush(wx.Brush(self.middle_brush_colour))
        self.dc.DrawArc(self.middle_x1, self.middle_y1, self.middle_x2, self.middle_y2, self.centre_x, self.centre_y)
        self.dc.SetBrush(wx.Brush(self.inner_brush_colour))
        self.dc.DrawArc(self.inner_x1, self.inner_y1, self.inner_x2, self.inner_y2, self.centre_x, self.centre_y)
