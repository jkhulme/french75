from biopepa_csv_parser import BioPepaCsvParser
from plotter import Plotter
import sys

"""
Central hub
Don't know whether this should be a class or not
"""

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
draw_plot.plot(results,parser)
