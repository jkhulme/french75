from biopepa_csv_parser import BioPepaCsvParser
from plotter import Plotter

parser = BioPepaCsvParser()
parser.openCsv('r_asrc.csv')
parser.parseResults()

draw_plot = Plotter()
draw_plot.plot(parser.results_dict)
