from ring import Ring
from circle import Circle


class LocationTree:

    def __init__(self, location_data):
        self.loc_data = location_data
        self.tree = {}
        self.queue = []
        self.circles = {}

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

        print self.tree

    def draw_tree_one(self, dc):
        r = 90
        self.circles['root'] = Ring((100, 100, r), (100, 100, 20), len(self.tree['root']), dc)
        self.circles['root'].paint()

        for key in self.tree['root']:
            self.queue += [key]
            new = self.circles['root'].give_birth(key)
            print new
            self.circles[key] = Circle(new, dc)
            self.circles[key].paint()
        self.output = []

        return self.output

    def draw_tree_two(self, dc):
        for key in self.loc_data:
            if (self.loc_data[key].l_type == 'membrane'):
                self.circles[key].paint()
                break

        self.queue += [self.tree['root'][0]]
        self.circles[self.tree['root'][0]].paint()
        self.output = []

        while (len(self.queue) > 0):
            node = self.queue.pop(0)
            print node
            self.output += [node]
            try:
                self.queue += self.tree[node]
                if (self.loc_data[node].l_type != 'membrane') and (self.loc_data[node].parent != 'root'):
                    self.circles[node].paint()
            except:
                self.circles[node].paint()

        return self.output
