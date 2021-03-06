from utils import rgb_to_hex, euclid_distance, rgba_to_rgb
from copy import deepcopy
from random import randrange
from numpy import std, mean
from itertools import groupby
from collections import Counter

_MIN_INTENSITY = 70
_MAX_INTENSITY = 255


class Line(object):

    def __init__(self, results, time, csv, key, colour, graph_width, graph_height, xmin, xmax, ymin, ymax):
        self.results = results
        self.original_results = results
        self.interpolated_results = []
        self.normalised_results = []
        self.original_time = time
        self.interpolated_time = []

        self.horizontal_scale = float(xmax - xmin) / graph_width
        self.vertical_scale = float(ymax - ymin) / graph_height

        self.length = self.calc_line_length(self.results, time)
        self.guide_points = 1000
        self.min = 0
        self.max = 0
        self.species = key
        self.plot_line = True
        self.intense_plot = False
        self.interpolated_results, self.interpolated_time = self.interpolate(self.results, time)
        self.interval = len(self.interpolated_results)/100
        self.rgb_tuple = colour
        self.flat_colour = rgb_to_hex(colour)
        self.thickness = 2
        self.colour_change_points = []
        self.seg_colour = None
        self.sub_plot_tuples = self.plot_sub_plots(self.interpolated_results, self.interval)
        self.past_points = []
        self.counter = 0
        self.normalised_sub_plots = []
        self.normalise()
        self.sub_lists = self.slice_lists(self.interpolated_results)
        self.debug_name = "Begin"

    def slice_lists(self, l):
        """
        Creates the string representation used for plots as queries
        """
        sub_lists = zip(l, l[1:], l[2:], l[3:], l[4:], l[5:], l[6:], l[7:])

        for i, sub_list in enumerate(sub_lists):
            l_mean = mean(sub_list)
            l_std = std(sub_list)
            sub_lists[i] = [(x - l_mean) / l_std for x in sub_list]

        for j, sub_list in enumerate(sub_lists):
            for i, element in enumerate(sub_list):
                if element < -0.43:
                    sub_list[i] = "a"
                elif element > 0.43:
                    sub_list[i] = "c"
                else:
                    sub_list[i] = "b"
            sub_lists[j] = ''.join(sub_list)

        return Counter([k for k, g in groupby(sub_lists)])

    def calc_line_length(self, results, time):
        """
        Need to know total length of the line for interpolation purposes
        Have to scale it from data space to visual space
        """
        data_time_points = zip(results, time)
        point_pairs = zip(data_time_points, data_time_points[1:])
        total_dist = 0

        for (point_a, point_b) in point_pairs:
            dist = euclid_distance(self.scale(point_a), self.scale(point_b))
            total_dist += dist

        return total_dist

    def scale(self, (x, y)):
        """
        convert from data space to visual space
        """
        return ((self.horizontal_scale*x, self.vertical_scale*y))

    def interpolate(self, results, time):
        """
        Handles the interpolation of points, need to test to make sure this is
        correct.  May have to advise that it is unsuitable for more than pretty
        pictures
        """
        data_time_points = zip(results, time)
        point_pairs = zip(data_time_points, data_time_points[1:])
        interpolated_data = []
        interpolated_time = []
        num_of_points = len(results)

        for ((data_a, time_a), (data_b, time_b)) in point_pairs:
            interpolated_data.append(data_a)
            interpolated_time.append(time_a)

            distance = euclid_distance(self.scale((data_a, time_a)), self.scale((data_b, time_b)))
            (scaled_data_a, scaled_time_a) = self.scale((data_a, time_a))
            (scaled_data_b, scaled_time_b) = self.scale((data_b, time_b))
            ratio = float(distance)/self.length
            interpolation_count = int((self.guide_points-num_of_points)*ratio)+1
            increment = (time_b - time_a)/float(interpolation_count)
            for i in range(1, interpolation_count):
                new_time = time_a + (i*increment)
                new_data = data_a + ((data_b - data_a) * ((new_time - time_a)/(time_b - time_a)))
                interpolated_data.append(new_data)
                interpolated_time.append(new_time)

            interpolated_data.append(data_b)
            interpolated_time.append(time_b)
        return (interpolated_data, interpolated_time)

    def plot_sub_plots(self, results, interval, debug=False):
        """
        Plots the sub plots and works out what colour the line should be
        this is for colour intensity plot
        """
        sub_plots = self.build_colour_plot_arrays(results, interval)
        sub_plot_tuples = []
        self.colour_change_points = []
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
            sub_plot_tuples.append((sub_plot, new_colour))
        self.seg_colour = self.colour_change_points[0][1]
        return sub_plot_tuples

    def build_colour_plot_arrays(self, results, interval):
        """
        Split the data into multiple lists padded with None to enable the intensity plot
        """
        plot_data = results
        plot_arrays = []
        self.min = min(plot_data)
        self.max = max(plot_data)
        count = 0
        while True:
            plot_arrays.append([None] * count + plot_data[count:count + interval] + [None] * (len(plot_data) - interval - count))
            if (plot_arrays[-1][-1] is not None):
                break
            count += interval - 1
        return plot_arrays

    def update_animation_colour(self, world_clock):
        """
        Traverse the list of time, colour tuples and the find which one is most current
        """
        max_time = False
        for i, (time, colour) in enumerate(self.colour_change_points[self.counter:]):
            if world_clock < self.interpolated_time[time]:
                if max_time:
                    self.seg_colour = colour
                    self.counter += i + 1
                    return
            else:
                max_time = True

    def random_colour(self):
        """
        The 50 closest to white are skipped to prevent pale colours
        """
        return (randrange(0, 200, 1),
                randrange(0, 200, 1),
                randrange(0, 200, 1))

    def normalise(self):
        """
        zero to one normalisation based on the max species in the session
        """
        d_max = max(self.results)
        d_min = min(self.results)
        for result in self.results:
            self.normalised_results.append((result - d_min) / float(d_max - d_min))
        for (sub_plot, colour) in self.sub_plot_tuples:
            new_sub_plot = []
            for data in sub_plot:
                if data is not None:
                    new_sub_plot.append((data-d_min)/float(d_max - d_min))
                else:
                    new_sub_plot.append(None)
            self.normalised_sub_plots.append((new_sub_plot, colour))

    def __copy__(self):
        """
        This is needed for deepcopy and copy stuff I think
        """
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        return result

    def __deepcopy__(self, memo):
        """
        Deepcopy stuff, used for copying the dictionary into the undo stack
        """
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result
