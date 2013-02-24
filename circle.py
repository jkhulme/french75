

class Circle:

    def __init__(self, details, dc):
        self.dc = dc
        self.x = details[0]
        self.y = details[1]
        self.radius = details[2]

    def paint(self):
        self.dc.DrawCircle(self.x, self.y, self.radius)

    def give_birth(self):
        radius = 10
        x = self.cell_x - radius
        y = self.cell_y - radius
        return (x, y, radius)
