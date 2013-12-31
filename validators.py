import wx


class TextNotEmptyValidator(wx.PyValidator):
    def __init__(self):
        wx.PyValidator.__init__(self)

    def Clone(self):
        return TextNotEmptyValidator()

    def Validate(self, win):
        textCtrl = self.GetWindow()
        text = textCtrl.GetValue()

        if not text:
            wx.MessageBox('validator error', 'Error')
            textCtrl.SetFocus()
            textCtrl.Refresh()
            return False
        else:
            return True

    def TransferToWindow(self):
        return True

    def TransferFromWindow(self):
        return True
