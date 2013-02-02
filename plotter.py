import matplotlib
matplotlib.use('WXAgg')
import matplotlib.pyplot as graph_plot

"""
Given the data, plot it on one graph
Might be doing to much work in here - maybe make it more abstract
"""


class Plotter():

    def __init__(self, axes, canvas):
        self.interval = 1
        self.axes = axes
        self.canvas = canvas

    def draw_figure(self):
        self.axes.clear()
        self.axes.plot([1, 2, 3, 4], [1, 4, 9, 16])
        self.canvas.draw()

    def plot(self, results, parser):
        self.axes.clear()
        for result in results:
            results_dict = results[result]
            for key in results_dict:
                if (not key == 'Time'):
                    self.axes.plot(results_dict['Time'], results_dict[key], label=key)

        #self.axes.ylabel('Process Count/Variable Value')
        #self.axes.xlabel('Time')
        self.axes.grid(True)
        self.axes.legend(loc=1)
        #self.axes.title('Active Src graph')
        xmin, xmax, ymin, ymax = self.axes.axis()
        self.axes.axis((parser.minx, parser.maxx, ymin, ymax))
        self.canvas.draw()

    def plot_colour_int(self, sub_plots):
        for sub_plot in sub_plots:
            graph_plot.plot(sub_plot)
        graph_plot.ylabel('Process Count/Variable Value')
        graph_plot.xlabel('Time')
        graph_plot.title('Active Src graph')
        graph_plot.show()

    def build_colour_plot_arrays(self, plot_data, interval):
        plot_arrays = []
        for i in range(0, len(plot_data) - 1):
            plot_arrays += [[None] * i + plot_data[i:i + interval] + [None] * (len(plot_data) - interval - i)]
        return plot_arrays
