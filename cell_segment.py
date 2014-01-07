import wx
from worldstate import WorldState


class CellSegment(object):

    """
    Used for drawing the animations.  There is one segment for each 'ring' in
    the cell.
    """

    def __init__(self, (tl_x, tl_y), radius, index, file_name, species):
        self.world = WorldState.Instance()
        self.counter = 0
        #Get an array of tuples of times when the colour changes and what
        #colour it changes to.
        num_of_segments = len(self.world.session_dict['tree_list'])
        change = 0
        self.sub_segments = []
        for i in range(0, num_of_segments):
            centre_x = tl_x
            centre_y = tl_y
            outer_x1, outer_y1 = centre_x + radius - change, centre_y
            outer_x2, outer_y2 = centre_x, 10 + change
            self.sub_segments.append((self.world.session_dict['lines'][file_name][species+"@"+self.world.session_dict['tree_list'][i]], self.world.session_dict['tree_list'][i], centre_x, centre_y, outer_x1, outer_y1, outer_x2, outer_y2))
            change += radius / num_of_segments

    def paint(self, dc):
        species_locations = ['whole_cell']
        for (line, location, centre_x, centre_y, outer_x1, outer_y1, outer_x2, outer_y2) in self.sub_segments:
            if location in species_locations or species_locations == ['whole_cell']:
                line.update_animation_colour(self.world.session_dict['clock'])
                dc.SetBrush(wx.Brush(line.seg_colour))
            else:
                dc.SetBrush(wx.Brush('white'))
            dc.DrawArc(outer_x1, outer_y1, outer_x2, outer_y2, centre_x, centre_y)

    def update_clock(self):
        pass
        """
        self.counter_inner = 0
        for (time, colour) in self.past_points_inner:
            if self.world.session_dict['clock'] >= time:
                self.counter_inner += 1
        self.past_points_inner = self.past_points_inner[:self.counter_inner]

        self.counter_middle = 0
        for (time, colour) in self.past_points_middle:
            if self.world.session_dict['clock'] >= time:
                self.counter_middle += 1
        self.past_points_middle = self.past_points_middle[:self.counter_middle]

        self.counter_outer = 0
        for (time, colour) in self.past_points_outer:
            if self.world.session_dict['clock'] >= time:
                self.counter_outer += 1
        self.past_points_outer = self.past_points_outer[:self.counter_outer]
        """
