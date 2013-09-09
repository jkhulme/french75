from location import Location
from locationtree import LocationTree
import re


class Biopepa_Model_Parser():

    def __init__(self):
        self.loc_results = {}
        self.loc_tree = {}

    def parse(self, path):
        self.open_model(path)
        self.get_locations()
        self.parse_location()

    def open_model(self, model):
        with open(model, 'r') as f:
            self.data = f.read()

    def get_locations(self):
        self.locations = []
        locations = re.findall("location (.*?)\n", self.data)
        for location in locations:
            self.locations.append("location " + location)

    def parse_location(self):
        for location in self.locations:
            print location
            try:
                loc_type = re.findall("type = (.*?);", location)[0].strip()
                loc_size = "Remove this"
                loc_name = re.findall("location (.*?) ", location)[0].strip()
                loc_parent = re.findall("in (.*?):", location)[0].strip() if len(re.findall("in (.*?):", location)) > 0 else "root"
                self.loc_results[loc_name] = Location(loc_name, loc_size,
                                                      loc_parent, loc_type)
            except:
                print "malformed location line: " + location

    def __str__(self):
        output = ""
        for location in self.loc_results:
            output += self.loc_results[location].__str__()
        return output

    def build_graph(self):
        self.tree = LocationTree(self.loc_results)
