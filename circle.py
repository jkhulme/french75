import random
from utils import euclid_distance


class Circle:

    def __init__(self, details, dc):
        self.dc = dc
        self.x = details[0]
        self.y = details[1]
        self.radius = details[2]
        self.children = []

    def paint(self):
        self.dc.DrawCircle(self.x, self.y, self.radius)

    def give_birth(self, node, num_of_children=2):
        radius = self.radius/float((num_of_children + 1.5))
        dist_flag = True
        while (dist_flag):
            if (random.random() < 0.5):
                x = self.x + (random.random() * (self.radius - (2 * radius)))
            else:
                x = self.x - (random.random() * (self.radius - (2 * radius)))

            if (random.random() < 0.5):
                y = self.y + (random.random() * (self.radius - (2 * radius)))
            else:
                y = self.y - (random.random() * (self.radius - (2 * radius)))

            if len(self.children) >= 1:
                for (child_x, child_y, child_radius) in self.children:
                    if (euclid_distance([x, y], [child_x, child_y]) > (radius + child_radius)):
                        dist_flag = False
            else:
                dist_flag = False

        child = (x, y, radius)
        self.children.append(child)

        return child
