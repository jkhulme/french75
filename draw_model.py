import wx
from biopepa_model_parser import Biopepa_Model_Parser


class Example():
    def __init__(self, frame):
        self.frame = frame

        self.frame.Bind(wx.EVT_PAINT, self.OnPaint)

        self.parser = Biopepa_Model_Parser()
        self.parser.open_model('camp-pka-mapk.biopepa')
        self.parser.get_locations()
        self.parser.parse_location()
        self.parser.build_graph()

        self.frame.Centre()
        self.frame.Show()

    def OnPaint(self, e):
        self.parser.tree.build_tree()
        self.tree = self.parser.tree.draw_tree()
        dc = wx.PaintDC(self.frame)
        y = 20
        for node in self.tree:
            dc.DrawCircle(50, y, 10)
            y += 30
