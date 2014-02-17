import wx


class Example(wx.Frame):

    def __init__(self, *args, **kwargs):
        super(Example, self).__init__(*args, **kwargs)

        self.InitUI()

    def InitUI(self):
        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        filem = fileMenu.Append(wx.ID_EXIT, 'Quit', 'Quit application')
        menubar.Append(fileMenu, '&File')
        self.SetMenuBar(menubar)

        self.Bind(wx.EVT_MENU, self.OnQuit, filem)

        self.SetSize((300, 200))
        self.SetTitle('simple menu')
        self.Centre()
        self.Show(True)

    def OnQuit(self, e):
        self.Close()

if __name__ == '__main__':
    ex = wx.App()
    Example(None)
    ex.MainLoop()
