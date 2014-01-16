from utils import rgb_to_hex, euclid_distance, rgba_to_rgb
from copy import deepcopy
from random import randrange

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

    def __init__(self, results, time, csv, key, colour, graph_width, graph_height, xmin, xmax, ymin, ymax):
        self.results = results
        self.time = time
        self.graph_width = graph_width
        self.graph_height = graph_height
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.horizontal_scale = float(xmax - xmin) / graph_width
        self.vertical_scale = float(ymax - ymin) / graph_height

        self.length = self.calc_line_length(self.results, self.time)

        self.guide_points = 1000
        #magic values - but they get changes
        self.min = 0
        self.max = 0
        self.species = key
        self.plot_line = True
        self.intense_plot = False
        #see issue 40 if interval is too high
        #TODO: make interval some function of number of points?
        self.interval = 10
        self.interpolate(self.results, self.time)
        #self.line_distance()
        self.rgb_tuple = colour
        self.flat_colour = rgb_to_hex(colour)
        self.thickness = 2
        self.colour_change_points = []
        self.seg_colour = None
        self.plot_sub_plots()
        self.time_points = []
        self.past_points = []
        self.counter = 0

    def calc_line_length(self, results, time):
        data_time_points = zip(results, time)
        point_pairs = zip(data_time_points, data_time_points[1:])
        total_dist = 0
        for (point_a, point_b) in point_pairs:
            dist = euclid_distance(self.scale(point_a), self.scale(point_b))
            total_dist += dist
        return total_dist

    def scale(self, (x, y)):
        return ((self.horizontal_scale*x, self.vertical_scale*y))

    """
    Handles the details of what needs to be done to interpolate.  Then
    updates the data to be used.

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

    """
    Handles the interpolation of points, need to test to make sure this is
    correct.  May have to advise that it is unsuitable for more than pretty
    pictures
    """
    def interpolate(self, results, time):
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
        self.results = interpolated_data
        self.time = interpolated_time


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
            #new_colour = rgb_to_hex(self.random_colour())
            self.colour_change_points.append((count, new_colour))
            self.sub_plot_tuples.append((sub_plot, new_colour))
        self.seg_colour = self.colour_change_points[0][1]

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

    def update_animation_colour(self, world_clock):
        max_time = False
        for i, (time, colour) in enumerate(self.colour_change_points[self.counter:]):
            if world_clock < self.time[time]:
                if max_time:
                    return
            else:
                max_time = True
                self.seg_colour = colour
                self.counter += i + 1

    def random_colour(self):
        """
        The 50 closest to white are skipped to prevent pale colours
        """
        return (randrange(0, 200, 1),
                randrange(0, 200, 1),
                randrange(0, 200, 1))

    def normalise(self):
        pass


    """
    Deepcopy stuff, used for copying the dictionary into the undo stack
    """
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
