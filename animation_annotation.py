class AnimationAnnotation():

    def __init__(self, text, start, end):
        self.x = None
        self.y = None
        self.text = text
        self.start = start
        self.end = end

    def set_position(self, (x, y)):
        self.x = x
        self.y = y

    def in_time(self, cur_time):
        if cur_time >= self.start and cur_time <= self.end:
            return True
        return False
