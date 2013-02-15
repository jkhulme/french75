

class Line(object):

    """
    self.axes
    self.results
    self.time
    self.intensity
    self.min_red
    self.max_red
    self.green
    self.blue
    self.min
    self.max
    self.csv
    self.species
    """

    def __init__(self, axes, results, time, csv, key):
        self.axes = axes
        self.results = results
        self.time = time
        self.intensity = False
        self.min_red = 0
        self.max_red = 255
        self.green = 0
        self.blue = 0
        self.min = 0
        self.max = 0
        self.csv = csv
        self.species = key
        self.showhide = True
        self.normal_plot = True
        self.interval = 2

    def __print__(self):
        print self.csv + self.results

    def plot(self):
        if self.showhide:
            if self.normal_plot:
                self.axes.plot(self.time, self.results, label=self.species)
            else:
                self.int_plot()

    def int_plot(self):
        self.build_colour_plot_arrays()
        self.plot_sub_plots()

    """
    Having trouble getting matplotlib to take an rgb tuple, so convert to hex which is working.
    Taken from this thread: http://stackoverflow.com/questions/214359/converting-hex-color-to-rgb-and-vice-versa
    """
    def rgb_to_hex(self, rgb):
        return '#%02x%02x%02x' % rgb

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
            self.axes.plot(self.time, sub_plot, color=self.rgb_to_hex(self.colour))

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
