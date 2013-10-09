import wx
from worldstate import WorldState


class CellSegment(object):

    def __init__(self, (tl_x, tl_y), radius, index, file_name, species):
        self.world = WorldState.Instance()
        #Get an array of tuples of times when the colour changes and what
        #colour it changes to.
        self.key = file_name
        print self.world.species_dict
        for i, (name, loc, l_flag) in enumerate(self.world.species_dict[species]):
            print name, loc, l_flag
            if l_flag == 1:
                print self.world.species_dict[species]
                self.species_inner = species+"@"+self.world.species_dict[species][i][1]
            elif l_flag == 2:
                self.species_middle = species+"@"+self.world.species_dict[species][i][1]
            elif l_flag == 3:
                self.species_outer = species+"@"+self.world.species_dict[species][i][1]

        self.result_inner = self.world.lines[self.key][self.species_inner]
        self.result_middle = self.world.lines[self.key][self.species_middle]
        self.result_outer = self.world.lines[self.key][self.species_outer]

        self.seg_colour_inner = self.result_inner.colour_change_points[0][1]
        self.seg_colour_middle = self.result_middle.colour_change_points[0][1]
        self.seg_colour_outer = self.result_outer.colour_change_points[0][1]

        self.time_points_inner = []
        self.time_points_middle = []
        self.time_points_outer = []

        self.past_points_inner = []
        self.past_points_middle = []
        self.past_points_outer = []

        self.counter_inner = 0
        self.counter_middle = 0
        self.counter_outer = 0

        for (time, colour) in self.result_inner.colour_change_points:
            self.time_points_inner.append(self.result_inner.time[time])
        for (time, colour) in self.result_middle.colour_change_points:
            self.time_points_middle.append(self.result_middle.time[time])
        for (time, colour) in self.result_outer.colour_change_points:
            self.time_points_outer.append(self.result_outer.time[time])

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
        if len(self.time_points_inner) > 0:
            if self.world.clock >= self.time_points_inner[self.counter_inner]:
                time = self.time_points_inner[self.counter_inner]
                self.seg_colour_inner = self.result_inner.colour_change_points[self.counter_inner][1]
                self.counter_inner += 1
                self.past_points_inner.append((time, self.seg_colour_inner))
        if len(self.time_points_middle) > 0:
            if self.world.clock >= self.time_points_middle[self.counter_middle]:
                time = self.time_points_middle[self.counter_middle]
                self.seg_colour_middle = self.result_middle.colour_change_points[self.counter_middle][1]
                self.counter_middle += 1
                self.past_points_middle.append((time, self.seg_colour_middle))
        if len(self.time_points_outer) > 0:
            if self.world.clock >= self.time_points_outer[self.counter_outer]:
                time = self.time_points_outer[self.counter_outer]
                self.seg_colour_outer = self.result_outer.colour_change_points[self.counter_outer][1]
                self.counter_outer += 1
                self.past_points_outer.append((time, self.seg_colour_outer))

        #eventually this will be done for each segment I think - once species are in multiple locations in cell i.e. nucleus, perinucleus etc
        dc.SetBrush(wx.Brush(self.seg_colour_outer))

        #The three arcs.  Drawn largest to smallest
        dc.DrawArc(self.outer_x1, self.outer_y1, self.outer_x2, self.outer_y2, self.centre_x, self.centre_y)

        dc.SetBrush(wx.Brush(self.seg_colour_middle))
        dc.DrawArc(self.middle_x1, self.middle_y1, self.middle_x2, self.middle_y2, self.centre_x, self.centre_y)

        dc.SetBrush(wx.Brush(self.seg_colour_inner))
        dc.DrawArc(self.inner_x1, self.inner_y1, self.inner_x2, self.inner_y2, self.centre_x, self.centre_y)

    def update_clock(self):
        self.counter = 0
        for (time, colour) in self.past_points:
            if self.world.clock >= time:
                self.counter += 1
        self.past_points = self.past_points[:self.counter]
