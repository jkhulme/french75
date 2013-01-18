import matplotlib.pyplot as graph_plot

class Plotter():

    def plot(self, results):
        for result in results:
            results_dict = results[result]
            for key in results_dict:
                if (not key == 'Time'):
                    graph_plot.plot(results_dict['Time'],results_dict[key], label=key)
                
        graph_plot.ylabel('Process Count/Variable Value')
        graph_plot.xlabel('Time')
        graph_plot.grid(True)
        graph_plot.legend(loc=1)
        graph_plot.title('Active Src graph')
        xmin,xmax,ymin,ymax = graph_plot.axis()
        graph_plot.axis((0,15000,ymin,ymax))
        graph_plot.show()
