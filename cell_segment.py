import wx
from worldstate import WorldState


class CellSegment(object):

    def __init__(self, (tl_x, tl_y), radius, dc, index):
        self.world = WorldState.Instance()

        self.key = self.world.lines.keys()[0]
        self.species = self.world.lines[self.key].keys()[index]
        self.result = self.world.lines[self.key][self.species]
        self.seg_colour = self.result.colour_change_points[0][1]
        self.time_points = []
        for (time, colour) in self.result.colour_change_points:
            self.time_points.append(self.result.time[time])

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
        #Work out whether we should change brush colour and what it should be set to
        if len(self.time_points) > 0:
            if self.world.clock >= self.time_points[0]:
                self.time_points.pop(0)
                self.seg_colour = self.result.colour_change_points.pop(0)[1]

        #eventually this will be done for each segment I think - once species are in multiple locations in cell i.e. nucleus, perinucleus etc
        self.dc.SetBrush(wx.Brush(self.seg_colour))

        #The three arcs.  Drawn largest to smallest
        self.dc.DrawArc(self.outer_x1, self.outer_y1, self.outer_x2, self.outer_y2, self.centre_x, self.centre_y)

        self.dc.DrawArc(self.middle_x1, self.middle_y1, self.middle_x2, self.middle_y2, self.centre_x, self.centre_y)

        self.dc.DrawArc(self.inner_x1, self.inner_y1, self.inner_x2, self.inner_y2, self.centre_x, self.centre_y)
