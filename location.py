

class Location():

    def __init__(self, name, size, parent, l_type):
        self.details = [name, size, parent, l_type]

    def __str__(self):
        return "name: {0}\nparent: {1}\ntype: {2}\nsize: {3}\n".format(self.details)
