from matplotlib.ticker import MultipleLocator
from worldstate import WorldState
from annotation import Annotation
from utils import rgb_to_hex
from matplotlib.patches import Ellipse


class Plotter(object):

    """
    Given the data, plot it on one graph

    Plots currently supported:
        Intensity plot.
        General line plots.
    """

    def __init__(self, axes):
        self.world = WorldState.Instance()
        self.axes = axes
        self.mpl_legend = False


    def plot(self):
        """
        Attempt to plot each line.
        Then set the environment of the graph
        """
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

        self.axes.xaxis.set_minor_locator(MultipleLocator(self.world.session_dict['xmax']*1.1/20))
        if self.world.session_dict['normalised']:
            self.axes.yaxis.set_minor_locator(MultipleLocator(1.1/20))
        else:
            self.axes.yaxis.set_minor_locator(MultipleLocator(self.world.session_dict['ymax']*1.1/20))

        self.axes.set_ylabel('Process Count/Variable Value')
        self.axes.set_xlabel('Time')
        self.axes.xaxis.grid(True, 'minor')
        self.axes.yaxis.grid(True, 'minor')
        self.axes.set_title(self.world.session_dict['title'])

        if self.world.session_dict['normalised']:
            self.axes.axis((self.world.session_dict['xmin'], self.world.session_dict['xmax'], 0, 1.1))
        else:
            self.axes.axis((self.world.session_dict['xmin'], self.world.session_dict['xmax'], self.world.session_dict['ymin'], self.world.session_dict['ymax']*1.1))

        if self.world.session_dict['draw_annotations']:
            self.redraw_annotations()

        #self.world.graph_canvas.draw()

        self.vertical_line()

    def redraw_annotations(self):
        """
        go through the list of annotations and plot them
        """
        for annotation in self.world.session_dict['annotations']:
            if not self.world.session_dict['normalised']:
                y1 = annotation.y1
                try:
                    y2 = annotation.y2
                except:
                    pass
                width=0.075*self.world.session_dict['ymax']
            else:
                y1 = annotation.y1 / self.world.session_dict['ymax']
                try:
                    y2 = annotation.y2 / self.world.session_dict['ymax']
                except:
                    pass
                width = 0.075
            if annotation.type == self.world._TEXT_ARROW:
                self.axes.annotate(annotation.text, xy=(annotation.x2, y2), xytext=(annotation.x1, y1), arrowprops=dict(facecolor=annotation.colour, shrink=0.05))
            elif annotation.type == self.world._ARROW:
                self.axes.annotate("", xy=(annotation.x2, y2), xytext=(annotation.x1, y1), arrowprops=dict(facecolor=annotation.colour, shrink=0.05))
            elif annotation.type == self.world._CIRCLE:
                circle1 = Ellipse((annotation.x1, y1), width=width, height=0.075*self.world.session_dict['xmax'], angle=90, facecolor='w', edgecolor=annotation.colour)
                self.axes.add_artist(circle1)
            elif annotation.type == self.world._TEXT:
                self.axes.text(annotation.x1, y1, annotation.text)

        #This is the arrow following mouse annotation thing
        if self.world.session_dict['temp_annotation'] is not None:
            annotation = self.world.session_dict['temp_annotation']
            self.axes.annotate("", xy=(annotation.x2, annotation.y2), xytext=(annotation.x1, annotation.y1), arrowprops=dict(facecolor=annotation.colour, shrink=0.05))

    def annotate_arrow(self, (x1, y1), (x2, y2), text="", colour="black"):
        self.axes.annotate(text, xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(facecolor=colour, shrink=0.05))
        self.world.session_dict['annotate'] = False
        if text:
            annotation = Annotation(self.world._TEXT_ARROW, (x1, y1), (x2, y2), text, colour)
        else:
            annotation = Annotation(self.world._ARROW, (x1, y1), (x2, y2))

        self.world.session_dict['annotations'].append(annotation)
        self.world.client.add_annotation(annotation)
        self.world.graph_canvas.draw()

    def annotate_text(self, (x, y), text="Annotation"):
        self.axes.text(x, y, text)
        annotation = Annotation(self.world._TEXT, (x, y), text=text)
        self.world.session_dict['annotate'] = False
        self.world.session_dict['annotations'].append(annotation)
        self.world.client.add_annotation(annotation)
        self.world.graph_canvas.draw()

    def annotate_circle(self, (x, y), colour="black"):
        circle1 = Ellipse((x, y), width=0.075*self.world.session_dict['ymax'], height=0.075*self.world.session_dict['xmax'], angle=90, facecolor='w', edgecolor=colour)
        annotation = Annotation(self.world._CIRCLE, (x, y), colour=colour)
        self.axes.add_artist(circle1)
        self.world.session_dict['annotate'] = False
        self.world.session_dict['annotations'].append(annotation)
        self.world.client.add_annotation(annotation)
        self.world.graph_canvas.draw()

    def vertical_line(self):
        """
        The sliding bar that follows the clock
        """
        if self.world.session_dict['normalised']:
            height = 1
        else:
            height = self.world.session_dict['ymax']

        self.axes.plot([self.world.session_dict['clock'], self.world.session_dict['clock']], [0, height], label="time_line", color='red', lw=3)
        self.world.graph_canvas.draw()
        self.axes.lines.pop()


    def plot_line(self, line):
        """
        Decides, for each line, how we're going to plot, normal or with intensities
        """
        if line.plot_line:
            if not self.world.session_dict['normalised']:
                if not line.intense_plot:
                    self.axes.plot(line.original_time, line.original_results, label=line.species, color=rgb_to_hex(line.rgb_tuple), alpha=1, lw=line.thickness)
                else:
                    for (sub_plot, new_colour) in line.sub_plot_tuples:
                        self.axes.plot(line.interpolated_time, sub_plot, color=new_colour, lw=line.thickness)
            else:
                if not line.intense_plot:
                    self.axes.plot(line.original_time, line.normalised_results, label=line.species, color=rgb_to_hex(line.rgb_tuple), alpha=1, lw=line.thickness)
                else:
                    for (sub_plot, new_colour) in line.normalised_sub_plots:
                        self.axes.plot(line.interpolated_time, sub_plot, color=new_colour, lw=line.thickness)
