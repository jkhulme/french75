import wx
import matplotlib
matplotlib.use('WXAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigCanvas


class French75(wx.Frame):

    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self,*args,**kwargs)
        self.Maximize()
        width, height = self.GetSize()
        print width, height

        main_panel = wx.Panel(self)

        self.graph_panel = wx.Panel(main_panel)
        self.model_panel = wx.Panel(main_panel)

        main_panel.SetBackgroundColour('white')
        self.model_panel.SetBackgroundColour('red')
        self.graph_panel.SetBackgroundColour('green')

        add_files_button = wx.Button(self.model_panel, -1, "Add")

        layout = wx.BoxSizer(wx.VERTICAL)
        layout.Add(self.graph_panel)
        layout.Add(self.model_panel)
        main_panel.SetSizerAndFit(layout)


        self.Bind(wx.EVT_SIZE, self.OnSize)

    def OnSize(self, event):
        print self.GetSize()
        self.graph_panel.SetSize(self.GetSize())

if __name__ == '__main__':
    app = wx.App()
    gui = French75(None)
    gui.Show()
    app.MainLoop()
