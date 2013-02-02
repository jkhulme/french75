import matplotlib
matplotlib.use('WXAgg')
import matplotlib.pyplot as graph_plot

"""
Given the data, plot it on one graph
Might be doing to much work in here - maybe make it more abstract
"""


class Plotter():

    def __init__(self):
        self.interval = 1
        self.data = [5, 6, 9, 14]

    def draw_figure(self, axes, canvas):
        x = range(len(self.data))
        axes.clear()
        axes.bar(left=x, height=self.data)
        canvas.draw()

    def plot(self, results, parser):
        for result in results:
            results_dict = results[result]
            for key in results_dict:
                if (not key == 'Time'):
                    graph_plot.plot(results_dict['Time'], results_dict[key], label=key)

        graph_plot.ylabel('Process Count/Variable Value')
        graph_plot.xlabel('Time')
        graph_plot.grid(True)
        graph_plot.legend(loc=1)
        graph_plot.title('Active Src graph')
        xmin, xmax, ymin, ymax = graph_plot.axis()
        graph_plot.axis((parser.minx, parser.maxx, ymin, ymax))
        graph_plot.show()

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
