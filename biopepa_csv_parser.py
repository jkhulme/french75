"""
Parse results data from BioPEPA csv files

Expected Structure
-algorithm used
-number of data points
-number of replications
-stop time
-start time
-line with "model paramaters" written
-run time
-column headings (Time needs to be first column)
-actual data
"""


class BioPepaCsvParser(object):

    """
    self.contents - entire file contents
    self.results_dict - the actual data indexed by column header, only for one csv
    self.keys - column headers, used to index the dictionary, time is included
    self.minx - start time
    self.maxx - stop time
    """

    def parse_results(self):
        data = self.contents[8:]

        for row in data:
            row = row.split(',')
            for i in range(0, len(row)):
                self.results_dict[self.keys[i]] += [float(row[i].strip())]

    def open_csv(self, csv):
        with open(csv, 'r') as f:
            self.contents = f.readlines()
            self.results_dict = {}
            self.keys = self.contents[7].split(',')
            self.keys[0] = self.keys[0][2:]
            self.results_dict[self.keys[0]] = []

            for i in range(1, len(self.keys)):
                self.keys[i] = self.keys[i].strip()[1:-1]
                self.results_dict[self.keys[i]] = []

    def timescale(self):
        self.minx = float(self.contents[4].strip()[14:])
        self.maxx = float(self.contents[3].strip()[13:])
