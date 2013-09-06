import random
from utils import euclid_distance


class Ring:

    def __init__(self, outer, inner, num_children, dc):
        self.dc = dc

        self.outer_x = outer[0]
        self.outer_y = outer[1]
        self.outer_radius = outer[2]

        self.inner_x = inner[0]
        self.inner_y = inner[1]
        self.inner_radius = inner[2]

        self.child_radius = ((self.outer_radius - self.inner_radius) / 2) - 3

        #mark the inner circle as a child to prevent other children overlapping
        #it
        self.children = [(self.inner_x, self.inner_y, self.inner_radius)]

    def paint(self):
        self.dc.DrawCircle(self.outer_x, self.outer_y, self.outer_radius)
        self.dc.DrawCircle(self.inner_x, self.inner_y, self.inner_radius)

    def give_birth(self, node):
        dist_flag = True
        while (dist_flag):
            dist_flag = False
            if (random.random() < 0.5):
                child_x = self.outer_x + (random.random() * (self.outer_radius - (2 * self.child_radius)))
            else:
                child_x = self.outer_x - (random.random() * (self.outer_radius - (2 * self.child_radius)))

            if (random.random() < 0.5):
                child_y = self.outer_y + (random.random() * (self.outer_radius - (2 * self.child_radius)))
            else:
                child_y = self.outer_y - (random.random() * (self.outer_radius - (2 * self.child_radius)))

            #checks for overlap between new child and any existing children
            #if there is overlap then rebirth the new child
            for (existing_x, existing_y, existing_radius) in self.children:
                if (euclid_distance([child_x, child_y], [existing_x, existing_y]) > (self.child_radius + self.existing_radius)):
                    dist_flag = False

        child = (child_x, child_y, self.child_radius)
        self.children.append(child)
        return child
