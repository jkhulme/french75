import random


class Circle:

    def __init__(self, details, dc):
        self.dc = dc
        self.x = details[0]
        self.y = details[1]
        self.radius = details[2]

    def paint(self):
        self.dc.DrawCircle(self.x, self.y, self.radius)

    def give_birth(self):
        radius = 13
        if (random.random() < 0.5):
            x = self.x + (random.random() * (self.radius - (2 * radius)))
        else:
            x = self.x - (random.random() * (self.radius - (2 * radius)))

        if (random.random() < 0.5):
            y = self.y + (random.random() * (self.radius - (2 * radius)))
        else:
            y = self.y - (random.random() * (self.radius - (2 * radius)))

        return (x, y, radius)
