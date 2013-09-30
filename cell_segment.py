import wx
from worldstate import WorldState


class CellSegment(object):

    def __init__(self, (tl_x, tl_y), radius, index):
        self.world = WorldState.Instance()

        #Get an array of tuples of times when the colour changes and what
        #colour it changes to.
        self.key = self.world.lines.keys()[0]
        self.species = self.world.lines[self.key].keys()[index]
        self.result = self.world.lines[self.key][self.species]
        self.seg_colour = self.result.colour_change_points[0][1]
        self.time_points = []
        for (time, colour) in self.result.colour_change_points:
            self.time_points.append(self.result.time[time])
        self.past_points = []
        self.counter = 0

        #Calculate the top and right points of the arc based on centre and
        #radius.  Arc goes CCW.

        self.centre_x, self.centre_y = tl_x, tl_y + radius

        self.outer_x1, self.outer_y1 = tl_x + radius, self.centre_y
        self.outer_x2, self.outer_y2 = tl_x, tl_y

        self.middle_x1, self.middle_y1 = tl_x + 2*(radius/3), self.centre_y
        self.middle_x2, self.middle_y2 = tl_x, tl_y + (radius/3)

        self.inner_x1, self.inner_y1 = tl_x + (radius/3), self.centre_y
        self.inner_x2, self.inner_y2 = tl_x, tl_y + 2*(radius/3)

    def paint(self, dc):
        #Work out whether we should change brush colour and what it should be set to
        if len(self.time_points) > 0:
            if self.world.clock >= self.time_points[self.counter]:
                time = self.time_points[self.counter]
                self.seg_colour = self.result.colour_change_points[self.counter][1]
                self.counter += 1
                self.past_points.append((time, self.seg_colour))

        #eventually this will be done for each segment I think - once species are in multiple locations in cell i.e. nucleus, perinucleus etc
        dc.SetBrush(wx.Brush(self.seg_colour))

        #The three arcs.  Drawn largest to smallest
        dc.DrawArc(self.outer_x1, self.outer_y1, self.outer_x2, self.outer_y2, self.centre_x, self.centre_y)

        dc.DrawArc(self.middle_x1, self.middle_y1, self.middle_x2, self.middle_y2, self.centre_x, self.centre_y)

        dc.DrawArc(self.inner_x1, self.inner_y1, self.inner_x2, self.inner_y2, self.centre_x, self.centre_y)
