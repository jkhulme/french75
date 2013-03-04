import random
from math import sqrt


class Circle:

    def __init__(self, details, dc):
        self.dc = dc
        self.x = details[0]
        self.y = details[1]
        self.radius = details[2]
        self.children = []

    def paint(self):
        self.dc.DrawCircle(self.x, self.y, self.radius)

    def euclid_distance(self, p1, p2):
        return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

    def give_birth(self, node):
        radius = self.radius/5
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
                print child
                if (self.euclid_distance([x, y], [child[0], child[1]]) > (2 * radius)):
                    print "ok"
                    flag = False
                else:
                    print "not ok"
                    flag = True
                print dist_flag
            dist_flag = flag

        self.children.append((x, y, radius))

        return (x, y, radius)
