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

    def draw_tree_one(self, dc):
        r = 90
        for key in self.loc_data:
            if (self.loc_data[key].l_type == 'membrane'):
                try:
                    num_children = len(self.tree[key])
                except:
                    num_children = 1
                self.circles[key] = Ring((100, 100, r), (100, 100, 60), num_children, dc)
                self.circles[key].paint()
                r = 60
                break

        self.queue += [self.tree['root'][0]]
        self.circles[self.tree['root'][0]] = Circle((100, 100, r), dc)
        self.circles[self.tree['root'][0]].paint()
        self.output = []

        while (len(self.queue) > 0):
            node = self.queue.pop(0)
            print node
            self.output += [node]
            try:
                self.queue += self.tree[node]
                if (self.loc_data[node].l_type != 'membrane') and (self.loc_data[node].parent != 'root'):
                    new = self.circles[self.loc_data[node].parent].give_birth(node)
                    self.circles[node] = Circle(new, dc)
                    print node
                    self.circles[node].paint()
            except:
                new = self.circles[self.loc_data[node].parent].give_birth(node)
                self.circles[node] = Circle(new, dc)
                self.circles[node].paint()

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
