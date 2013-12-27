from line import Line
from utils import euclid_distance
from random import randrange
from matplotlib.ticker import MultipleLocator
import matplotlib.pyplot as plt
from worldstate import WorldState
from annotation import Annotation


class Plotter(object):

    """
    Given the data, plot it on one graph

    Plots currently supported:
        Intensity plot.
        General line plots.

    self.axes - Lines are plotted using this.
    self.world.session_dict['graph_canvas'] - Used to draw the axes/plots
    self.parser - the csv parser
    self.world.session_dict['redraw_legend'] - do we need to redraw the legend or not
    """

    """
    Initialise what we need, and then create a line for each plot
    """
    def __init__(self, axes):
        self.world = WorldState.Instance()
        self.axes = axes
        self.parser = self.world.session_dict['parser']
        self.mpl_legend = False
        self.colours = []
        self.hard_colours = self.populate_colours()
        self.draw_annotations = True

        """
        Create a line from each species.  Don't put time in there.
        """
        for result in self.world.session_dict['results']:
            results_dict = self.world.session_dict['results'][result]
            self.world.session_dict['lines'][result] = {}
            for key in results_dict:
                if (not key == 'Time'):
                    self.world.session_dict['lines'][result][key] = Line(self.axes,
                                                     results_dict[key],
                                                     results_dict['Time'],
                                                     result, key,
                                                     self.choose_colour())
        self.world.session_dict['lines'] = self.world.session_dict['lines']

    """
    Attempt to plot each line.
    Then set the environment of the graph
    """
    def plot(self):
        self.axes.clear()

        for result in self.world.session_dict['lines']:
            for key in self.world.session_dict['lines'][result]:
                self.world.session_dict['lines'][result][key].plot()

        #my interactive legend
        if (self.world.session_dict['redraw_legend']):
            self.world.session_dict['legend'].draw_legend(self, self.world.session_dict['lines'])

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
        self.axes.set_title(self.world.session_dict['title'])
        self.axes.axis((self.parser.xmin, self.parser.xmax, self.parser.ymin, self.parser.ymax*1.1))

        if self.draw_annotations:
            self.redraw_annotations()

        self.world.session_dict['graph_canvas'].draw()

    def redraw_annotations(self):
        for annotation in self.world.session_dict['annotations']:
            if annotation.type == self.world._TEXT_ARROW:
                self.axes.annotate(annotation.text, xy=(annotation.x2, annotation.y2), xytext=(annotation.x1, annotation.y1), arrowprops=dict(facecolor=annotation.colour, shrink=0.05))
            elif annotation.type == self.world._ARROW:
                self.axes.annotate("", xy=(annotation.x2, annotation.y2), xytext=(annotation.x1, annotation.y1), arrowprops=dict(facecolor=annotation.colour, shrink=0.05))
            elif annotation.type == self.world._CIRCLE:
                circle1 = plt.Circle((annotation.x1, annotation.y1), 0.2, facecolor='w', edgecolor=annotation.colour)
                self.axes.add_artist(circle1)
            elif annotation.type == self.world._TEXT:
                self.axes.text(annotation.x1, annotation.y1, annotation.text)
        if self.world.session_dict['temp_annotation'] is not None:
            annotation = self.world.session_dict['temp_annotation']
            self.axes.annotate("", xy=(annotation.x2, annotation.y2), xytext=(annotation.x1, annotation.y1), arrowprops=dict(facecolor=annotation.colour, shrink=0.05))

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

    def vertical_line(self):
        self.axes.plot([self.world.session_dict['clock'], self.world.session_dict['clock']], [0, 120000], label="time_line", color='red', lw=3)
        self.world.session_dict['graph_canvas'].draw()
        self.axes.lines.pop()
