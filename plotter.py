from matplotlib.ticker import MultipleLocator
import matplotlib.pyplot as plt
import matplotlib.collections as mpl_collections
from worldstate import WorldState
from annotation import Annotation
from utils import rgb_to_hex
import time

class Plotter(object):

    """
    Given the data, plot it on one graph

    Plots currently supported:
        Intensity plot.
        General line plots.

    self.axes - Lines are plotted using this.
    self.world.graph_canvas - Used to draw the axes/plots
    self.parser - the csv parser
    self.mpl_legend - used when saving the graph
    """

    def __init__(self, axes):
        self.world = WorldState.Instance()
        self.axes = axes
        self.mpl_legend = False

    """
    Attempt to plot each line.
    Then set the environment of the graph
    """
    def plot(self):
        self.axes.clear()

        for result in self.world.session_dict['lines']:
            for key in self.world.session_dict['lines'][result]:
                self.plot_line(self.world.session_dict['lines'][result][key])

        #my interactive legend
        if (self.world.session_dict['redraw_legend']):
            self.world.legend.draw_legend()

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
        self.axes.axis((self.world.session_dict['xmin'], self.world.session_dict['xmax'], self.world.session_dict['ymin'], self.world.session_dict['ymax']*1.1))

        if self.world.session_dict['draw_annotations']:
            self.redraw_annotations()

        self.world.graph_canvas.draw()

    def redraw_annotations(self):
        """
        go through the list of annotations and plot them
        """
        for annotation in self.world.session_dict['annotations']:
            if annotation.show:
                if annotation.type == self.world._TEXT_ARROW:
                    self.axes.annotate(annotation.text, xy=(annotation.x2, annotation.y2), xytext=(annotation.x1, annotation.y1), arrowprops=dict(facecolor=annotation.colour, shrink=0.05))
                elif annotation.type == self.world._ARROW:
                    self.axes.annotate("", xy=(annotation.x2, annotation.y2), xytext=(annotation.x1, annotation.y1), arrowprops=dict(facecolor=annotation.colour, shrink=0.05))
                elif annotation.type == self.world._CIRCLE:
                    circle1 = plt.Circle((annotation.x1, annotation.y1), 0.2, facecolor='w', edgecolor=annotation.colour)
                    self.axes.add_artist(circle1)
                elif annotation.type == self.world._TEXT:
                    self.axes.text(annotation.x1, annotation.y1, annotation.text)
        #This is the arrow following mouse annotation thing
        if self.world.session_dict['temp_annotation'] is not None:
            annotation = self.world.session_dict['temp_annotation']
            self.axes.annotate("", xy=(annotation.x2, annotation.y2), xytext=(annotation.x1, annotation.y1), arrowprops=dict(facecolor=annotation.colour, shrink=0.05))

    """
    The following 3 methods create the annotations, and plot them for the
    first time
    """
    def annotate_arrow(self, (x1, y1), (x2, y2), text="", colour="black"):
        self.axes.annotate(text, xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(facecolor=colour, shrink=0.05))
        self.world.session_dict['annotate'] = False
        if text:
            self.world.session_dict['annotations'].append(Annotation(self.world._TEXT_ARROW, (x1, y1), (x2, y2), text, colour))
        else:
            self.world.session_dict['annotations'].append(Annotation(self.world._ARROW, (x1, y1), (x2, y2)))
        self.world.graph_canvas.draw()

    def annotate_text(self, (x, y), text="Annotation"):
        self.axes.text(x, y, text)
        self.world.session_dict['annotate'] = False
        self.world.session_dict['annotations'].append(Annotation(self.world._TEXT, (x, y), text=text))
        self.world.graph_canvas.draw()

    def annotate_circle(self, (x, y), colour="black"):
        circle1 = plt.Circle((x, y), 0.2, facecolor='w', edgecolor=colour)
        self.axes.add_artist(circle1)
        self.world.session_dict['annotate'] = False
        self.world.session_dict['annotations'].append(Annotation(self.world._CIRCLE, (x, y), colour))
        self.world.graph_canvas.draw()

    def vertical_line(self):
        """
        The sliding bar that follows the clock
        """
        self.axes.plot([self.world.session_dict['clock'], self.world.session_dict['clock']], [0, 120000], label="time_line", color='red', lw=3)
        self.world.graph_canvas.draw()
        self.axes.lines.pop()

    """
    Decides, for each line, how we're going to plot, normal or with intensities
    """
    def plot_line(self, line):
        if line.plot_line:
            #t0 = time.time()
            if line.plot_state == 0:
                self.world.graph_axes.plot(line.original_time, line.original_results, label=line.species, color=rgb_to_hex(line.rgb_tuple), alpha=1, lw=line.thickness)
            elif line.plot_state == 1:
                self.world.graph_axes.set_xlim(self.world.session_dict['xmin'], self.world.session_dict['xmax'])
                self.world.graph_axes.set_ylim(self.world.session_dict['ymin'], self.world.session_dict['ymax'])
                #segments = []
                #colours = []
                """
                Seems to be faster to just plot the lines separately rather than using line collection
                """
                for (sub_plot, new_colour) in line.sub_plot_tuples:
                    #segments.append(zip(line.time, sub_plot))
                    #colours.append(new_colour)
                    self.world.graph_axes.plot(line.interpolated_time, sub_plot, color=new_colour, lw=line.thickness)
                #lines = mpl_collections.LineCollection(segments, linewidths=line.thickness, colors=colours)
                #self.world.graph_axes.add_collection(lines)
                #1.22244095802s
            elif line.plot_state == 2:
                print "Normalised data"
                self.world.graph_axes.plot(line.original_time, line.normalised_results, label=line.species, color=rgb_to_hex(line.rgb_tuple), alpha=1, lw=line.thickness)
            #t1 = time.time()
            #print t1 - t0
