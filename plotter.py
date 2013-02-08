from line import Line

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
            print result
            results_dict = results[result]
            for key in results_dict:
                if (not key == 'Time'):
                    self.results[key] = Line(self.axes, results_dict[key], results_dict['Time'], result)
                    print self.results[key]

    """
    For basic matplotlib line graphs.
    """
    def plot(self):
        self.axes.clear()
        for key in self.results:
            self.results[key].plot()

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
