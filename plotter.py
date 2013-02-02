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

        self.axes.set_ylabel('Process Count/Variable Value')
        self.axes.set_xlabel('Time')
        self.axes.grid(True)
        self.axes.legend(loc=1)
        self.axes.set_title('Active Src graph')
        xmin, xmax, ymin, ymax = self.axes.axis()
        self.axes.axis((parser.minx, parser.maxx, ymin, ymax))
        self.canvas.draw()

    def plot_colour_int(self, sub_plots):
        for sub_plot in sub_plots:
            self.axes.plot(sub_plot)
        self.axes.set_ylabel('Process Count/Variable Value')
        self.axes.set_xlabel('Time')
        self.axes.set_title('Active Src graph')
        self.canvas.draw()

    def build_colour_plot_arrays(self, plot_data, interval):
        plot_arrays = []
        for i in range(0, len(plot_data) - 1):
            plot_arrays += [[None] * i + plot_data[i:i + interval] + [None] * (len(plot_data) - interval - i)]
        return plot_arrays
