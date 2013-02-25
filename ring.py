import math


class Ring:

    def __init__(self, outer, inner, dc):
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
        new_x = (self.child_x * math.cos(math.radians(20))) - (self.child_y * math.sin(math.radians(20)))
        new_y = (self.child_x * math.sin(math.radians(20))) + (self.child_y * math.cos(math.radians(20)))
        return (new_x, new_y, self.child_radius)
