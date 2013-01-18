from biopepa_csv_parser import BioPepaCsvParser
from plotter import Plotter
import sys

results = {}
sys.argv = sys.argv[1:]
for arg in sys.argv:
    parser = BioPepaCsvParser()
    parser.openCsv(arg)
    parser.parseResults()
    results[arg] = parser.results_dict
    parser.timeScale()

draw_plot = Plotter()
draw_plot.plot(results,parser)
