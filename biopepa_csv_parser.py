import re
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

    def __init__(self):
        self.ymin = 1000000
        self.minx = 1000000
        self.ymax = 0
        self.maxx = 0

    def open_csv(self, csv):
        with open(csv, 'r') as f:
            contents = f.read().strip()
            results = {}
            results['simulator'] = re.findall('Simulator: (.*?)\n', contents)[0]
            results['datapoints'] = re.findall('Number of data points: (.*?)\n', contents)[0]
            results['replications'] = re.findall('Number of independent replications: (.*?)\n', contents)[0]
            results['stop_time'] = re.findall('Stop time: (.*?)\n', contents)[0]
            results['start_time'] = re.findall('Start time: (.*?)\n', contents)[0]
            results['run_time'] = re.findall('Run time = (.*?)\n', contents)[0]
            results['data'] = ('Time, ' + re.findall('Time, (.*?)\n', contents)[0]).split(',')
            data = [line.split(',') for line in contents.split('\n') if not "#" in line]
            transposed_data = map(None, *data)
            print transposed_data
            results['results'] = {}
            for i, data_item in enumerate(results['data']):
                results['results'][str(data_item)] = [float(n) for n in transposed_data[i]]

            print results['results']['Time']
            self.results_dict = results['results']

    def parse_results(self):
        pass

    def timescale(self):
        self.minx = float(self.results_dict['start_time'])
        self.maxx = float(self.results_dict['stop_time'])

    def values(self):
        for result in self.results_dict:
            if not result == 'Time':
                if min(self.results_dict[result]) < self.ymin:
                    self.ymin = min(self.results_dict[result])
                if max(self.results_dict[result]) > self.ymax:
                    self.ymax = max(self.results_dict[result])
            else:
                if min(self.results_dict[result]) < self.minx:
                    self.minx = min(self.results_dict[result])
                if max(self.results_dict[result]) > self.maxx:
                    self.maxx = max(self.results_dict[result])


class BioPepaCsvParserOld(object):

    """
    self.contents - entire file contents
    self.results_dict - the actual data indexed by column header, only for one csv
    self.keys - column headers, used to index the dictionary, time is included
    self.minx - start time
    self.maxx - stop time
    """

    def __init__(self):
        self.ymin = 1000000
        self.minx = 1000000
        self.ymax = 0
        self.maxx = 0

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

    def values(self):
        for result in self.results_dict:
            if not result == 'Time':
                if min(self.results_dict[result]) < self.ymin:
                    self.ymin = min(self.results_dict[result])
                if max(self.results_dict[result]) > self.ymax:
                    self.ymax = max(self.results_dict[result])
            else:
                if min(self.results_dict[result]) < self.minx:
                    self.minx = min(self.results_dict[result])
                if max(self.results_dict[result]) > self.maxx:
                    self.maxx = max(self.results_dict[result])
