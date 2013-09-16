import wx

class LargePlotDialog(wx.Dialog):

    def __init__(self, *args, **kw):
        super(LargePlotDialog, self).__init__(*args, **kw)
        (dispW, dispH) = wx.DisplaySize()
        self.SetSize((dispW/1.1, dispH/1.1))
        self.Centre()
