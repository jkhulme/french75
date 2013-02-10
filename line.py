

class Line():

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
        self.min_red = 150
        self.max_red = 255
        self.green = 0
        self.blue = 0
        self.min = 0
        self.max = 0
        self.csv = csv
        self.species = key

    def __print__(self):
        print self.csv + self.results

    def plot(self):
        self.axes.plot(self.time, self.results, label=self.species)

    def show_hide(self):
        print "help"

    """
    def plot_sub_plots(self, sub_plots):
        for sub_plot in sub_plots:
            count = 0
            current = 0
            while True:
                if (sub_plot[count] != None):
                    current = sub_plot[count]
                    break
                count += 1
            self.r = (((current - self.min) / float(self.max - self.min)) * (self.max_red - self.min_red)) + self.min_red
            self.colour = (self.r, self.green, self.blue)
            self.axes.plot(sub_plot, color=self.rgb_to_hex(self.colour))
    """
    """
    Split the data into multiple lists padded with None to enable the intensity plot
    """
    """
    def build_colour_plot_arrays(self, plot_data, interval):
        for i, x in enumerate(plot_data):
            plot_data[i] = float(x)
        plot_arrays = []
        self.min = min(plot_data)
        self.max = max(plot_data)
        count = 0
        while True:
            plot_arrays += [[None] * count + plot_data[count:count + interval] + [None] * (len(plot_data) - interval - count)]
            if (plot_arrays[-1][-1] != None):
                break
            count += interval - 1
        return plot_arrays
    """