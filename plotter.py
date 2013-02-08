"""
Given the data, plot it on one graph

Plots currently supported:
    Intensity plot.
    General line plots.

Might be doing to much work in here - maybe make it more abstract
"""


class Plotter():
    #self.interval - should be 2, used to split the datasets for intensity plots
    #self.axes - Lines are plotted using this.
    #self.canvas - Used to draw the axes/plots
    #self.min_red - min red for colour intensity
    #self.max_red - max red for colour intensity
    #self.green - green component for colour intensity
    #self.blue - blue component for colour intensity
    #self.min - minimum data value - used in colour intensity
    #self.max - maximum data value used in colour intensity
    #self.r - calculated red component for colour intensity

    def __init__(self, axes, canvas, results, parser):
        self.interval = 2
        self.axes = axes
        self.canvas = canvas
        self.min_red = 150
        self.max_red = 255
        self.green = 0
        self.blue = 0
        self.min = 0
        self.max = 0
        self.parser = parser
        self.results = {}
        for result in results:
            results_dict = results[result]
            for key in results_dict:
                if (not key == 'Time'):
                    self.results[key] = (results_dict['Time'], results_dict[key])

    """
    For basic matplotlib line graphs.
    """
    def plot(self):
        self.axes.clear()
        for key in self.results:
            if (not key == 'Time'):
                self.axes.plot(self.results[key][0], self.results[key][1], label=key)

        self.axes.set_ylabel('Process Count/Variable Value')
        self.axes.set_xlabel('Time')
        self.axes.grid(True)
        self.axes.legend(loc=1)
        self.axes.set_title('Active Src graph')
        xmin, xmax, ymin, ymax = self.axes.axis()
        self.axes.axis((self.parser.minx, self.parser.maxx, ymin, ymax))
        self.canvas.draw()

    """
    Having trouble getting matplotlib to take an rgb tuple, so convert to hex which is working.
    Taken from this thread: http://stackoverflow.com/questions/214359/converting-hex-color-to-rgb-and-vice-versa
    """
    def rgb_to_hex(self, rgb):
        return '#%02x%02x%02x' % rgb

    """
    Change the colour depending on data gradient.
    Currently a bit iffy.
    """
    def plot_colour_int(self):
        self.axes.clear()
        for key in self.results:
            if (not key == 'Time'):
                sub_plots = self.build_colour_plot_arrays(self.results[key][1], self.interval)
                self.spread = self.max - self.min
                self.plot_sub_plots(sub_plots)

        self.axes.set_ylabel('Process Count/Variable Value')
        self.axes.set_xlabel('Time')
        self.axes.set_title('Active Src graph')
        self.canvas.draw()

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
    Split the data into multiple lists padded with None to enable the intensity plot
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
