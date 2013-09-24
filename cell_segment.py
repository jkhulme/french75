import wx
from worldstate import WorldState


class CellSegment(object):

    def __init__(self, (tl_x, tl_y), radius, dc):
        self.world = WorldState.Instance()
        if self.world.first_circle:
            key = self.world.lines.keys()[0]
            species = self.world.lines[key].keys()[0]
            print self.world.lines[key][species].colour_change_points
            print self.world.lines[key][species].time
            self.world.seg_colour = self.world.lines[key][species].colour_change_points[0][1]
            self.world.time_points = []
            for (time, colour) in self.world.lines[key][species].colour_change_points:
                self.world.time_points.append(self.world.lines[key][species].time[time])
            self.world.first_circle = False

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
        key = self.world.lines.keys()[0]
        species = self.world.lines[key].keys()[0]

        print "time"
        print self.world.time_points
        print "clock"
        print self.world.clock
        if self.world.clock >= self.world.time_points[0]:
            self.world.time_points.pop(0)
            self.world.seg_colour = self.world.lines[key][species].colour_change_points.pop(0)[1]
            print self.world.seg_colour
        self.dc.SetBrush(wx.Brush(self.world.seg_colour))
        self.dc.DrawArc(self.outer_x1, self.outer_y1, self.outer_x2, self.outer_y2, self.centre_x, self.centre_y)
        self.dc.DrawArc(self.middle_x1, self.middle_y1, self.middle_x2, self.middle_y2, self.centre_x, self.centre_y)
        self.dc.DrawArc(self.inner_x1, self.inner_y1, self.inner_x2, self.inner_y2, self.centre_x, self.centre_y)
