

class LocationTree:

    def __init__(self, location_data):
        self.loc_data = location_data
        self.tree = {}
        self.queue = []

    def build_tree(self):
        for loc in self.loc_data:
            if (not self.loc_data[loc].parent in self.tree):
                self.tree[self.loc_data[loc].parent] = [self.loc_data[loc].name]
            else:
                self.tree[self.loc_data[loc].parent] += [self.loc_data[loc].name]
        print self.tree

    def draw_tree(self):
        self.queue += [self.tree['root'][0][:-1]]
        while (len(self.queue) > 0):
            node = self.queue.pop(0)
            print node
            try:
                self.queue += self.tree[node]
            except:
                print "leaf"
