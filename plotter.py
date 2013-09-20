from line import Line
from utils import euclid_distance
from random import randrange
from matplotlib.ticker import MultipleLocator
try:
    from xkcd import XKCDify
except:
    print "scipy not installed"
from worldstate import WorldState

"""
Given the data, plot it on one graph

Plots currently supported:
    Intensity plot.
    General line plots.
"""


class Plotter(object):

    """
    self.axes - Lines are plotted using this.
    self.canvas - Used to draw the axes/plots
    self.parser - the csv parser
    self.results - the results data
    self.redraw_legend - do we need to redraw the legend or not
    self.legend - Will plot the legend
    """

    """
    Initialise what we need, and then create a line for each plot
    """
    def __init__(self, axes, canvas, results, parser, legend, redraw_legend, xkcdify):
        self.world = WorldState.Instance()
        self.axes = axes
        self.canvas = canvas
        self.parser = parser
        self.legend = legend
        self.results = {}
        self.redraw_legend = redraw_legend
        self.mpl_legend = False
        self.colours = []
        self.hard_colours = self.populate_colours()
        self.xkcdify = xkcdify

        """
        Create a line from each species.  Don't put time in there.
        """
        for result in results:
            results_dict = results[result]
            self.results[result] = {}
            for key in results_dict:
                if (not key == 'Time'):
                    self.results[result][key] = Line(self.axes,
                                                     results_dict[key],
                                                     results_dict['Time'],
                                                     result, key,
                                                     self.choose_colour())
        self.world.lines = self.results

    """
    Attempt to plot each line.
    Then set the environment of the graph
    """
    def plot(self):
        self.axes.clear()

        for result in self.results:
            for key in self.results[result]:
                self.results[result][key].plot()

        #my interactive legend
        if (self.redraw_legend):
            self.legend.draw_legend(self, self.results)

        #matplotlib legend - for saving with a legend
        if (self.mpl_legend):
            self.axes.legend()

        #Grid lines - TODO - make these not fixed
        self.axes.xaxis.set_minor_locator(MultipleLocator(500))
        self.axes.yaxis.set_minor_locator(MultipleLocator(5000))

        self.axes.set_ylabel('Process Count/Variable Value')
        self.axes.set_xlabel('Time')
        self.axes.xaxis.grid(True, 'minor')
        self.axes.yaxis.grid(True, 'minor')
        self.axes.set_title('Graph')
        self.axes.axis((self.parser.xmin, self.parser.xmax, self.parser.ymin, self.parser.ymax*1.1))

        self.canvas.draw()

    """
    Work through the list of set colours first.  Then start generating new
    colours - if they are too close then regenerate
    """
    def choose_colour(self):
        if (len(self.hard_colours) > 0):
            return self.hard_colours.pop()
        else:
            accept = False

            while(not accept):
                accept = True
                temp_colour = self.random_colour()
                for colour in self.colours:
                    if (euclid_distance(temp_colour, colour) < 50):
                        accept = False
                        break
            self.colours.append(temp_colour)
            return temp_colour

    def random_colour(self):
        return (randrange(0, 200, 1),
                randrange(0, 200, 1),
                randrange(0, 200, 1))

    def populate_colours(self):
        return [(255, 0, 0),
                (0, 255, 0),
                (0, 0, 255)]
