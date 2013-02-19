from location import Location
from locationtree import LocationTree


class Biopepa_Model_Parser():

    def __init__(self):
        self.loc_results = {}
        self.loc_tree = {}

    def open_model(self, model):
        with open(model, 'r') as f:
            self.data = f.readlines()

    def get_locations(self):
        self.locations = []
        for line in self.data:
            if (line.split(' ')[0] == 'location'):
                self.locations += [line.strip()]

    def parse_location(self):
        for location in self.locations:
            loc_type = location.split(',')[1].strip()
            loc_type = loc_type[7:-1]
            loc_size = location.split(',')[0].split('size')[1].strip()[2:]
            loc_name = location.split(',')[0].strip()
            if ('in' in loc_name):
                loc_name = loc_name.split('in')[0].strip()[9:]
                loc_parent = location.split(',')[0].strip().split('in')[1].strip().split(':')[0]
            else:
                loc_name = location.split(',')[0].strip().split(':')[0][9:].strip()
                loc_parent = "root"
            self.loc_results[loc_name] = Location(loc_name, loc_size,
                loc_parent, loc_type)

    def __str__(self):
        output = ""
        for location in self.loc_results:
            output += self.loc_results[location].__str__()
        return output

    def build_graph(self):
        self.tree = LocationTree(self.loc_results)

"""
if __name__ == '__main__':
    parser = Biopepa_Model_Parser()
    parser.open_model('camp-pka-mapk.biopepa')
    parser.get_locations()
    parser.parse_location()
    print parser
    parser.build_graph()
"""