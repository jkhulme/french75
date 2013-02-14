

class LocationTree:

    def __init__(self, location_data):
        self.loc_data = location_data
        self.tree = {}

    def build_tree(self):
        self.root_elems()
        self.child_elems()

    def root_elems(self):
        for loc in self.loc_data:
            if (self.loc_data[loc].parent == "root"):
                self.tree[self.loc_data[loc].name] = {}
        print self.tree

    def child_elems(self):
        for loc in self.loc_data:
            if (self.loc_data[loc].parent in self.tree.keys()):
                self.tree[self.loc_data[loc].name] = {}
