import math


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

    def paint(self):
        self.dc.DrawCircle(self.x, self.y, self.radius)

    def give_birth(self):
        translatedx = self.child_x - self.x
        translatedy = self.child_y - self.y
        new_x = (translatedx * math.cos(math.radians(self.theta))) - (translatedy * math.sin(math.radians(self.theta)))
        new_y = (translatedx * math.sin(math.radians(self.theta))) + (translatedy * math.cos(math.radians(self.theta)))
        new_x += self.x
        new_y += self.y
        self.theta += self.theta_base
        return (new_x, new_y, self.child_radius)
