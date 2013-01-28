import wx


class GraphFrame(wx.Frame):

    def __init__(self, *args, **kwargs):
        super(GraphFrame, self).__init__(*args, **kwargs)

        self.launchGui()

    def launchGui():
        print "wow"
