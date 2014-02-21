class Location():

    def __init__(self, name, size, parent, l_type):
        self.name = name
        self.size = size
        self.parent = parent
        self.l_type = l_type

    def __str__(self):
        return "name: " + self.name + "\nparent: " + self.parent + "\ntype: " + self.l_type + "\nsize: " + self.size + "\n"
