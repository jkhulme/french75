from location import Location
from locationtree import LocationTree
import re


class Biopepa_Model_Parser():

    def __init__(self):
        self.loc_results = {}
        self.loc_tree = {}
        self.tree = None

    def parse(self, path):
        data = self.open_model(path)
        locations = self.get_locations(data)
        self.parse_location(locations)

    def open_model(self, model):
        with open(model, 'r') as f:
            data = f.read()
        return data

    def get_locations(self, data):
        locations = []
        location_lines = re.findall("location (.*?)\n", data)
        for location in location_lines:
            locations.append("location " + location)
        return locations

    def parse_location(self, locations):
        for location in locations:
            try:
                loc_type = re.findall("type = (.*?);", location)[0].strip()
                loc_size = "Remove this"
                loc_name = re.findall("location (.*?) ", location)[0].strip()
                loc_parent = re.findall("in (.*?):", location)[0].strip() if len(re.findall("in (.*?):", location)) > 0 else "root"
                if loc_name != "mechanisms":
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
        return self.tree.build_tree()

