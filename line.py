from math import sqrt


class Line(object):

    """
    self.axes - plots the data
    self.results - data to plot
    self.time - The time scale
    self.min_red - for intensity plot
    self.max_red - for intensity plot
    self.r - what shade of red should be used in the intensity plot
    self.colour - holds the rgb tuple for plot colour
    self.green - for intensity plot
    self.blue - for intensity plot
    self.min - minimum data value
    self.max - maximum data value
    self.csv - file the data came from
    self.species - species the data is results of
    self.showhide - whether to display or not on the axes
    self.intense_plot - whether to do colour intensity or normal plot
    self.interval - for building sub plots - I think this has to be 2.
    """

    def __init__(self, axes, results, time, csv, key):
        self.axes = axes
        self.results = results
        self.time = time
        self.min_red = 0
        self.max_red = 255
        self.green = 0
        self.blue = 0
        self.min = 0
        self.max = 0
        self.csv = csv
        self.species = key
        self.showhide = True
        self.intense_plot = False
        self.interval = 2

    def __str__(self):
        return self.csv + "\n" + self.results

    def euclid_distance(self, p1, p2):
        return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

    def line_distance(self):
        output = []
        for i in range(0, len(self.results) - 1):
            p1 = (float(self.time[i]), float(self.results[i]))
            p2 = (float(self.time[i + 1]), float(self.results[i + 1]))
            output += [self.euclid_distance(p1, p2)]
        print output

    def interpolate(self, data, steps):
        middle = []
        inc = (data[1] - data[0]) / float(steps)
        for i in range(0, steps - 1):
            middle += [data[0] + ((i + 1) * inc)]
        print [data[0]] + middle + [data[1]]

    """
    Decides how we're going to plot
    """
    def plot(self):
        self.interpolate([1, 2], 2)
        self.interpolate([1, 2], 3)
        self.interpolate([4, 8], 2)
        self.interpolate([4, 8], 3)
        self.interpolate([4, 8], 4)
        self.interpolate([4, 8], 5)
        if self.showhide:
            if not self.intense_plot:
                self.axes.plot(self.time, self.results, label=self.species)
            else:
                self.int_plot()

    """
    performs the steps for intensity plot
    """
    def int_plot(self):
        self.build_colour_plot_arrays()
        self.plot_sub_plots()

    """
    Having trouble getting matplotlib to take an rgb tuple, so convert to hex which is working.
    Taken from this thread: http://stackoverflow.com/questions/214359/converting-hex-color-to-rgb-and-vice-versa
    """
    def rgb_to_hex(self, rgb):
        return '#%02x%02x%02x' % rgb

    """
    Plots the sub plots and works out what colour the line should be
    this is for colour intensity plot
    """
    def plot_sub_plots(self):
        sub_plots = self.plot_arrays
        for sub_plot in sub_plots:
            count = 0
            current = 0
            while True:
                if (sub_plot[count] != None):
                    current = sub_plot[count]
                    break
                count += 1
            self.r = (((current - self.min) / float(self.max - self.min)) * (self.max_red - self.min_red)) + self.min_red
            self.colour = (self.r, self.r, self.r)
            self.axes.plot(self.time, sub_plot, '.', color=self.rgb_to_hex(self.colour))

    """
    Split the data into multiple lists padded with None to enable the intensity plot
    """
    def build_colour_plot_arrays(self):
        plot_data = self.results
        for i, x in enumerate(plot_data):
            plot_data[i] = float(x)
        self.plot_arrays = []
        self.min = min(plot_data)
        self.max = max(plot_data)
        count = 0
        while True:
            self.plot_arrays += [[None] * count + plot_data[count:count + self.interval] + [None] * (len(plot_data) - self.interval - count)]
            if (self.plot_arrays[-1][-1] != None):
                break
            count += self.interval - 1
        return self.plot_arrays
