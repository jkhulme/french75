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

    def draw_tree(self, dc):
        r = 90
        for key in self.loc_data:
            if (self.loc_data[key].l_type == 'membrane'):
                self.circles[key] = Ring((100, 100, r), (100, 100, 60), len(self.tree[key]), dc)
                self.circles[key].paint()
                r = 60
                break

        self.queue += [self.tree['root'][0]]
        self.circles['extra'] = Circle((100, 100, r), dc)
        self.circles['extra'].paint()
        self.output = []

        while (len(self.queue) > 0):
            node = self.queue.pop(0)
            self.output += [node]
            try:
                self.queue += self.tree[node]
                if (self.loc_data[node].l_type != 'membrane') and (self.loc_data[node].parent != 'root'):
                    new = self.circles[self.loc_data[node].parent].give_birth()
                    self.circles[node] = Circle(new, dc)
                    self.circles[node].paint()
            except:
                new = self.circles[self.loc_data[node].parent].give_birth()
                self.circles[node] = Circle(new, dc)
                self.circles[node].paint()

        return self.output
