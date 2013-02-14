

class LocationTree:

    def __init__(self, location_data):
        self.loc_data = location_data
        self.tree = {}
        self.stack = []

    def build_tree(self):
        for loc in self.loc_data:
            if (not self.loc_data[loc].parent in self.tree):
                self.tree[self.loc_data[loc].parent] = [self.loc_data[loc].name]
            else:
                self.tree[self.loc_data[loc].parent] += [self.loc_data[loc].name]
        print self.tree

    def draw_tree(self):
        self.stack += [self.tree['root'][0][:-1]]
        while (len(self.stack) > 0):
            node = self.stack.pop(0)
            print node
            try:
                self.stack += self.tree[node]
            except:
                print "leaf"
