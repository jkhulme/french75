"""
Given the data, plot it on one graph
Might be doing to much work in here - maybe make it more abstract
"""


class Plotter():

    def __init__(self, axes, canvas):
        self.interval = 1
        self.axes = axes
        self.canvas = canvas
        self.min_red = 160
        self.max_red = 255
        self.green = 0
        self.blue = 0
        self.min = 0
        self.max = 0

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

    def rgb_to_hex(self, rgb):
        return '#%02x%02x%02x' % rgb

    def plot_colour_int(self, sub_plots):
        self.spread = self.max - self.min
        for sub_plot in sub_plots:
            count = 0
            current = 0
            while True:
                if (sub_plot[count] != None):
                    current = sub_plot[count]
                    break
                count += 1
            self.r = (((current - self.min) / float(self.max - self.min)) * (self.max_red - self.min_red)) + self.min_red
            self.colour = (self.r, self.green, self.blue)
            self.axes.plot(sub_plot, color=self.rgb_to_hex(self.colour))
        self.axes.set_ylabel('Process Count/Variable Value')
        self.axes.set_xlabel('Time')
        self.axes.set_title('Active Src graph')
        self.canvas.draw()

    def build_colour_plot_arrays(self, results, interval):
        plot_data = []
        for result in results:
            results_dict = results[result]
            for key in results_dict:
                if (not key == 'Time'):
                    plot_data = results_dict[key]

        print plot_data
        for i, x in enumerate(plot_data):
            plot_data[i] = float(x)

        plot_arrays = []
        self.min = min(plot_data)
        self.max = max(plot_data)
        count = 0
        while True:
            plot_arrays += [[None] * count + plot_data[count:count + interval] + [None] * (len(plot_data) - interval - count)]
            if (plot_arrays[-1][-1] != None):
                break
            count += interval - 1
        return plot_arrays
