import wx
from worldstate import WorldState


class CellSegment(object):

    """
    Used for drawing the animations.  There is one segment for each 'ring' in
    the cell.
    """

    def __init__(self,(tl_x, tl_y), radius, index, file_name, species):
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
            line = self.world.session_dict['lines'][file_name].get(species+"@"+self.world.session_dict['tree_list'][i], None)
            self.sub_segments.append((line, self.world.session_dict['tree_list'][i], centre_x, centre_y, outer_x1, outer_y1, outer_x2, outer_y2))
            change += radius / num_of_segments

    def paint(self, dc, p_id):
        species_locations = ['whole_cell']
        for (line, location, centre_x, centre_y, outer_x1, outer_y1, outer_x2, outer_y2) in self.sub_segments:
            if line != None:
                if location in species_locations or species_locations == ['whole_cell']:
                    line.update_animation_colour(self.world.session_dict['clock'])
                    dc.SetBrush(wx.Brush(line.seg_colour))
            else:
                dc.SetBrush(wx.Brush('white'))
            dc.DrawArc(outer_x1, outer_y1, outer_x2, outer_y2, centre_x, centre_y)
        for annotation in self.world.session_dict['anime_annotations'].get(p_id,[]):
            if annotation.in_time(self.world.session_dict['clock']):
                dc.DrawCircle(annotation.x, annotation.y, 10)

    def update_clock(self):
        for (line, location, centre_x, centre_y, outer_x1, outer_y1, outer_x2, outer_y2) in self.sub_segments:
            line.counter = 0
