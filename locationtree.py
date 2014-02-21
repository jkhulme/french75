class LocationTree:

    def __init__(self, location_data):
        self.loc_data = location_data
        self.tree = {}
        self.queue = []
        self.circles = {}

    """
    Last paragraph needs to be done in model reader probably
    """
    def build_tree(self):
        self.tree = {}
        for loc in self.loc_data:
            if (not self.loc_data[loc].parent in self.tree):
                self.tree[self.loc_data[loc].parent] = [self.loc_data[loc].name]
            else:
                self.tree[self.loc_data[loc].parent] += [self.loc_data[loc].name]
        old_root = self.tree['root'][0]
        self.tree['root'] = self.tree[old_root]
        self.tree.pop(old_root, None)
        for location_name in self.tree['root']:
            self.loc_data[location_name].parent = 'root'
        return self.tree

    def __str__(self):
        return self.tree.__str__()
