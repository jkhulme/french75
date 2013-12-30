from math import ceil
from utils import rgb_to_hex, euclid_distance, rgba_to_rgb
from copy import deepcopy

_MIN_INTENSITY = 70
_MAX_INTENSITY = 255


class Line(object):

    """
    self.world.graph_axes - plots the data
    self.results - data to plot
    self.time - The time scale
    self.colour - holds the rgb tuple for plot colour
    self.species - species the data is results of
    self.plot_line - whether to display or not on the axes
    self.intense_plot - whether to do colour intensity or normal plot
    self.interval - for building sub plots - I think this has to be 2
    """

    def __init__(self, results, time, csv, key, colour):
        self.results = results
        self.time = time
        #magic values - but they get changes
        self.min = 0
        self.max = 0
        self.species = key
        self.plot_line = True
        self.intense_plot = False
        #see issue 40 if interval is too high
        #TODO: make interval some function of number of points?
        self.interval = 20
        self.line_distance()
        self.rgb_tuple = colour
        self.flat_colour = rgb_to_hex(colour)
        self.thickness = 2
        self.colour_change_points = []
        self.plot_sub_plots()

    """
    Handles the details of what needs to be done to interpolate.  Then
    updates the data to be used.
    """
    def line_distance(self):
        dist = (ceil(self.time[-1]) / len(self.results)) * 1.1
        output_time = []
        output_results = []
        for i in range(0, len(self.results) - 1):
            p1 = (self.time[i], self.results[i])
            p2 = (self.time[i + 1], self.results[i + 1])
            if (euclid_distance(p1, p2) > dist):
                step = ceil(euclid_distance(p1, p2) / dist)
                output_time.extend([self.time[i]] + self.interpolate([self.time[i], self.time[i + 1]], step))
                output_results.extend([self.results[i]] + self.interpolate([self.results[i], self.results[i + 1]], step))
            else:
                output_time.append(self.time[i])
                output_results.append(self.results[i])
        output_time.append(self.time[-1])
        output_results.append(self.results[-1])
        self.time = output_time
        self.results = output_results

    """
    Handles the interpolation of points, need to test to make sure this is
    correct.  May have to advise that it is unsuitable for more than pretty
    pictures
    """
    def interpolate(self, data, steps):
        middle = []
        inc = (data[1] - data[0]) / float(steps)
        for i in range(0, int(steps) - 1):
            middle += [data[0] + ((i + 1) * inc)]
        return middle

    """
    Plots the sub plots and works out what colour the line should be
    this is for colour intensity plot
    """
    def plot_sub_plots(self):
        sub_plots = self.build_colour_plot_arrays()
        self.sub_plot_tuples = []
        for sub_plot in sub_plots:
            count = 0
            current = 0
            while True:
                if (sub_plot[count] is not None):
                    current = sub_plot[count]
                    break
                count += 1
            intensity = (((current - self.min) / float(1 + self.max - self.min)) * (_MAX_INTENSITY - _MIN_INTENSITY)) + _MIN_INTENSITY
            alpha = intensity/255
            new_colour = rgb_to_hex(rgba_to_rgb(self.rgb_tuple, alpha))
            self.colour_change_points.append((count, new_colour))
            self.sub_plot_tuples.append((sub_plot, new_colour))


    """
    Split the data into multiple lists padded with None to enable the intensity plot
    """
    def build_colour_plot_arrays(self):
        plot_data = self.results
        plot_arrays = []
        self.min = min(plot_data)
        self.max = max(plot_data)
        count = 0
        while True:
            plot_arrays.append([None] * count + plot_data[count:count + self.interval] + [None] * (len(plot_data) - self.interval - count))
            if (plot_arrays[-1][-1] is not None):
                break
            count += self.interval - 1
        return plot_arrays

    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        return result

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result
