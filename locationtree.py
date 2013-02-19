

class LocationTree:

    def __init__(self, location_data):
        self.loc_data = location_data
        self.tree = {}
        self.queue = []

    def build_tree(self):
        self.tree = {}
        for loc in self.loc_data:
            if (not self.loc_data[loc].parent in self.tree):
                self.tree[self.loc_data[loc].parent] = [self.loc_data[loc].name]
            else:
                self.tree[self.loc_data[loc].parent] += [self.loc_data[loc].name]

    def draw_tree(self):
        self.queue += [self.tree['root'][0]]
        self.output = []
        while (len(self.queue) > 0):
            node = self.queue.pop(0)
            self.output += [node]
            try:
                self.queue += self.tree[node]
            except:
                pass
        return self.output
