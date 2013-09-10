import re
"""
Parse results data from BioPEPA csv files

Expected Structure
-algorithm used
-number of data points
-number of replications
-stop time
-start time
-line with "model paramaters" wrten
-run time
-column headings (Time needs to be first column)
-actual data
"""


class BioPepaCsvParser(object):

    def __init__(self):
        self.ymin = 1000000
        self.xmin = 1000000
        self.ymax = 0
        self.xmax = 0
        self.results_dict = {}

    """
    Returns a dictionary - 1 key for each species, and 1 for time, returning an array of integers.
    i.e. {"foo": [1,4,9,16,25], "bar":[1,8,27,64,125], "Time":[1,2,3,4,5]}
    """
    def parse_csv(self, csv):
        with open(csv, 'r') as f:
            contents = f.read().strip()
            self.results_dict['simulator'] = re.findall('Simulator: (.*?)\n', contents)[0]
            self.results_dict['datapoints'] = re.findall('Number of data points: (.*?)\n', contents)[0]
            self.results_dict['replications'] = re.findall('Number of independent replications: (.*?)\n', contents)[0]
            self.results_dict['stop_time'] = re.findall('Stop time: (.*?)\n', contents)[0]
            self.results_dict['start_time'] = re.findall('Start time: (.*?)\n', contents)[0]
            self.results_dict['run_time'] = re.findall('Run time = (.*?)\n', contents)[0]
            self.results_dict['data'] = ('Time, ' + re.findall('Time, (.*?)\n', contents)[0]).split(',')
            data = [line.split(',') for line in contents.split('\n') if not "#" in line]
            transposed_data = map(None, *data)
            self.results_dict['results'] = {}
            for i, data_item in enumerate(self.results_dict['data']):
                self.results_dict['results'][str(data_item)] = [float(n) for n in transposed_data[i]]

            self.results_dict = self.results_dict['results']
            self.min_max_values()

    """
    To get the labels for the axis
    """
    def min_max_values(self):
        for result in self.results_dict:
            if not result == 'Time':
                self.ymin = min(self.ymin, min(self.results_dict[result]))
                self.ymax = max(self.ymax, max(self.results_dict[result]))
            else:
                self.xmin = min(self.xmin, min(self.results_dict[result]))
                self.xmax = max(self.xmax, max(self.results_dict[result]))
