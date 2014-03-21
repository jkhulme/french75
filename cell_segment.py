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
        num_of_segments = len(self.world.session_dict['tree_list'])
        change = 0
        self.sub_segments = []

        for i in range(0, num_of_segments):
            centre_x = tl_x
            centre_y = tl_y

            outer_x1, outer_y1 = centre_x + radius - change, centre_y
            outer_x2, outer_y2 = centre_x, 10 + change



            self.sub_segments.append((file_name, species, i, self.world.session_dict['tree_list'][i], centre_x, centre_y, outer_x1, outer_y1, outer_x2, outer_y2))

            change += radius / num_of_segments

    def paint(self, dc, p_id):
        species_locations = ['whole_cell']

        for (file_name, species, i, location, centre_x, centre_y, outer_x1, outer_y1, outer_x2, outer_y2) in self.sub_segments:
            line = self.world.session_dict['lines'][file_name].get(species+"@"+self.world.session_dict['tree_list'][i], None)
            if line != None:
                if location in species_locations or species_locations == ['whole_cell']:
                    line.update_animation_colour(self.world.session_dict['clock'])
                    dc.SetBrush(wx.Brush(line.seg_colour))
            else:
                dc.SetBrush(wx.Brush('white'))
            dc.DrawArc(outer_x1, outer_y1, outer_x2, outer_y2, centre_x, centre_y)
        dc.SetBrush(wx.Brush('black'))

        for annotation in self.world.session_dict['anime_annotations'].get(p_id,[]):
            #Draw the labels
            if annotation.in_time(self.world.session_dict['clock']):
                dc.SetBrush(wx.Brush('white'))
                dc.DrawCircle(annotation.x, annotation.y, 10)
                dc.SetBrush(wx.Brush('black'))
                dc.DrawLabel(str(annotation.a_id), (annotation.x-4, annotation.y-7, 5, 5), alignment=wx.ALIGN_LEFT|wx.ALIGN_TOP)

    def update_clock(self):
        for (line, location, centre_x, centre_y, outer_x1, outer_y1, outer_x2, outer_y2) in self.sub_segments:
            line.counter = 0
