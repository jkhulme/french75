from biopepa_csv_parser import BioPepaCsvParser
from plotter import Plotter
import sys


#results - one index for each csv file, dictionary of dictionaries
#argv - files passed to plotted

results = {}
argv = sys.argv[1:]
for arg in argv:
    parser = BioPepaCsvParser()
    parser.openCsv(arg)
    parser.parseResults()
    results[arg] = parser.results_dict
    parser.timeScale()

draw_plot = Plotter()
draw_plot.plot(results, parser)
subs = draw_plot.build_colour_plot_arrays([1, 2, 3, 4, 5, 6], 2)
draw_plot.plot_colour_int(subs)


#if name == main
