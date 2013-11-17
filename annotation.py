class Annotation(object):

    def __init__(self, a_type, start, finish=None, text="", colour="black"):
        self.type = a_type
        (self.x1, self.y1) = start
        if finish:
            (self.x2, self.y2) = finish
        if text:
            self.text = text
        self.colour = colour
