import uuid


class Annotation(object):

    """
    does all four types of arrow.
    An array of these is stored in the worldstate
    """

    def __init__(self, a_type, start, finish=None, text="", colour="black", normalised=False):
        self.id = uuid.uuid4()
        self.type = a_type
        (self.x1, self.y1) = start
        if finish:
            (self.x2, self.y2) = finish
        if text:
            self.text = text
        self.colour = colour
        self.show = True
        self.normalised = normalised

    def __eq__(self, other):
        return self.id == other.id
