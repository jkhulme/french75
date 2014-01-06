import wx


class CellSegments2(object):

    def __init__(self, tree, (width, height)):
        tree_list = self.tree_to_list(tree)
        num_of_segments = len(tree.keys())
        radius = height - 20
        change = 0
        self.sub_segments = []
        for i in range(0, num_of_segments):
            centre_x = (width-height)/2
            centre_y = height - 10
            outer_x1, outer_y1 = centre_x + radius - change, centre_y
            outer_x2, outer_y2 = centre_x, 10 + change
            self.sub_segments.append((tree_list[i], centre_x, centre_y, outer_x1, outer_y1, outer_x2, outer_y2))
            change += radius / num_of_segments

    def paint(self, dc, species_locations):

        #Draws CCW
        for (location, centre_x, centre_y, outer_x1, outer_y1, outer_x2, outer_y2) in self.sub_segments:
            print location
            print species_locations
            if location in species_locations[:-1] or species_locations == ['whole_cell']:
                dc.SetBrush(wx.Brush('green'))
            else:
                dc.SetBrush(wx.Brush('white'))
            dc.DrawArc(outer_x1, outer_y1, outer_x2, outer_y2, centre_x, centre_y)
        #centre_x, centre_y, outer_x1, outer_y1, outer_x2, outer_y2 = self.sub_segments[0]
        #dc.DrawArc(outer_x1, outer_y1, outer_x2, outer_y2, centre_x, centre_y)

    def tree_to_list(self, tree):
        next_key = 'root'
        tree_list = []
        while True:
            next_key = tree.get(next_key, [None])[0]
            if next_key is None:
                break
            tree_list.append(next_key)
        return tree_list
