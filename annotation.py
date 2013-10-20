class Annotation(object):

    def __init__(self, type, start, finish=None, text="",):
        self.type = type
        (self.x1, self.y1) = start
        if finish:
            (self.x2, self.y2) = finish
        if text:
            self.text = text
