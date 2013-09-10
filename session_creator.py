import wx

class SessionDialog(wx.Dialog):

    def __init__(self, *args, **kw):
        super(SessionDialog, self).__init__(*args, **kw)
        (dispW, dispH) = wx.DisplaySize()
        self.SetSize((dispW/4, dispH/2))
        self.Centre()
