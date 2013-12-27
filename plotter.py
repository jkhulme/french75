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


        """
        Create a line from each species.  Don't put time in there.
        """


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

        if self.world.session_dict['draw_annotations']:
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

    def annotate_arrow(self, (x1, y1), (x2, y2), text="", colour="black"):
        self.axes.annotate(text, xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(facecolor=colour, shrink=0.05))
        self.world.session_dict['annotate'] = False
        if text:
            self.world.session_dict['annotations'].append(Annotation(self.world._TEXT_ARROW, (x1, y1), (x2, y2), text, colour))
        else:
            self.world.session_dict['annotations'].append(Annotation(self.world._ARROW, (x1, y1), (x2, y2)))
        self.world.session_dict['graph_canvas'].draw()

    def annotate_text(self, (x, y), text="Annotation"):
        self.axes.text(x, y, text)
        self.world.session_dict['annotate'] = False
        self.world.session_dict['annotations'].append(Annotation(self.world._TEXT, (x, y), text=text))
        self.world.session_dict['graph_canvas'].draw()

    def annotate_circle(self, (x, y), colour="black"):
        circle1 = plt.Circle((x, y), 0.2, facecolor='w', edgecolor=colour)
        self.axes.add_artist(circle1)
        self.world.session_dict['annotate'] = False
        self.world.session_dict['annotations'].append(Annotation(self.world._CIRCLE, (x, y), colour))
        self.world.session_dict['graph_canvas'].draw()

    def vertical_line(self):
        self.axes.plot([self.world.session_dict['clock'], self.world.session_dict['clock']], [0, 120000], label="time_line", color='red', lw=3)
        self.world.session_dict['graph_canvas'].draw()
        self.axes.lines.pop()
