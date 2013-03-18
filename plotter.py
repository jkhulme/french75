from line import Line
from math import sqrt
from random import randrange
from xkcd import XKCDify

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
    self.draw_legend - redrawing the legend is causing a seg fault on mac, I think it is something to do with redefining the event handler
    self.legend - Will plot the legend
    """

    """
    Initialise what we need, and then create a line for each plot
    """
    def __init__(self, axes, canvas, results, parser, legend, draw_legend):
        self.axes = axes
        self.canvas = canvas
        self.parser = parser
        self.legend = legend
        self.results = {}
        self.draw_legend = draw_legend
        self.mpl_legend = False
        self.colours = []
        self.hard_colours = self.populate_colours()

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

    """
    Attempt to plot each line.
    Then set the environment of the graph
    """
    def plot(self):
        self.axes.clear()
        for result in self.results:
            for key in self.results[result]:
                self.results[result][key].plot()
        if (self.draw_legend):
            self.legend.draw_legend(self, self.results)

        if (self.mpl_legend):
            self.axes.legend()

        self.axes.set_ylabel('Process Count/Variable Value')
        self.axes.set_xlabel('Time')
        self.axes.grid(True)
        self.axes.set_title('Active Src graph')
        xmin, xmax, ymin, ymax = self.axes.axis()
        self.axes.axis((self.parser.minx, self.parser.maxx, ymin, ymax))

        XKCDify(self.axes, xaxis_loc=0.0, yaxis_loc=1.0,
                xaxis_arrow='+-', yaxis_arrow='+-',
                expand_axes=True)

        self.canvas.draw()

    def choose_colour(self):
        if (len(self.hard_colours) > 0):
            return self.hard_colours.pop()
        else:
            accept = False

            while(not accept):
                accept = True
                temp_colour = self.random_colour()
                for colour in self.colours:
                    if (self.euclid_distance(temp_colour, colour) < 50):
                        accept = False
                        break
            self.colours.append(temp_colour)
            return temp_colour

    def random_colour(self):
        rgb = [0, 0, 0]
        for i in range(0, 3):
            rgb[i] = randrange(0, 200, 1)
        rgb_tup = (rgb[0], rgb[1], rgb[2])
        return rgb_tup

    def euclid_distance(self, p1, p2):
        return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2 + (p1[2] - p2[2]) ** 2)

    def populate_colours(self):
        colour_list = []
        colour_list.append((255, 0, 0))
        colour_list.append((0, 255, 0))
        colour_list.append((0, 0, 255))
        return colour_list
