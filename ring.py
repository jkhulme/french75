import random
from utils import euclid_distance


class Ring:

    def __init__(self, outer, inner, num_children, dc):
        self.theta = 360 / (num_children)
        self.theta_base = 360 / (num_children)
        self.dc = dc
        self.x = outer[0]
        self.y = outer[1]
        self.radius = outer[2]
        self.cell_x = inner[0]
        self.cell_y = inner[1]
        self.cell_radius = inner[2]
        self.child_x = self.cell_x + self.cell_radius - ((self.radius - self.cell_radius) / 4)
        self.child_y = self.cell_y + self.cell_radius - ((self.radius - self.cell_radius) / 4)
        self.child_radius = ((self.radius - self.cell_radius) / 2) - 3
        #self.child_radius = 10
        self.children = [(self.cell_x, self.cell_y, self.cell_radius)]

    def paint(self):
        print "painting"
        self.dc.DrawCircle(self.x, self.y, self.radius)
        self.dc.DrawCircle(self.cell_x, self.cell_y, self.cell_radius)

    def give_birth(self, node):
        radius = self.child_radius
        dist_flag = True
        while (dist_flag):
            flag = False
            if (random.random() < 0.5):
                x = self.x + (random.random() * (self.radius - (2 * radius)))
            else:
                x = self.x - (random.random() * (self.radius - (2 * radius)))

            if (random.random() < 0.5):
                y = self.y + (random.random() * (self.radius - (2 * radius)))
            else:
                y = self.y - (random.random() * (self.radius - (2 * radius)))

            for child in self.children:
                if (euclid_distance([x, y], [child[0], child[1]]) > (2 * radius)):
                    flag = False
                else:
                    flag = True
            dist_flag = flag

        self.children.append((x, y, radius))

        return (x, y, radius)
