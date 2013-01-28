from biopepa_csv_parser import BioPepaCsvParser
from plotter import Plotter
from gui_launcher import VisWindow
import sys
import wx


#results - one index for each csv file, dictionary of dictionaries
#argv - files passed to plotted

"""
results = {}
argv = sys.argv[1:]



app = wx.App()
gui = VisWindow(None)
app.MainLoop()

print gui.paths


draw_plot = Plotter()
draw_plot.plot(results, parser)
subs = draw_plot.build_colour_plot_arrays([1, 2, 3, 4, 5, 6], 2)
draw_plot.plot_colour_int(subs)
"""


class French75(wx.Frame):

    def __init__(self, *args, **kwargs):
        super(French75, self).__init__(*args, **kwargs)

        self.launchGui()

    def launchGui(self):
        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        filem = fileMenu.Append(wx.ID_OPEN, '&Open')
        menubar.Append(fileMenu, '&File')
        self.SetMenuBar(menubar)

        self.Bind(wx.EVT_MENU, self.openFile, filem)

        self.SetSize((500, 300))
        self.SetTitle('French75')
        self.Centre()
        self.Show(True)

    def openFile(self, e):
        file_chooser = wx.FileDialog(
            self,
            message="Choose a file",
            wildcard="*.csv",
            style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR
            )
        if file_chooser.ShowModal() == wx.ID_OK:
            self.paths = file_chooser.GetPaths()
        file_chooser.Destroy()


if __name__ == '__main__':
    app = wx.App()
    gui = French75(None)
    app.MainLoop()
