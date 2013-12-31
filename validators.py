import wx


class TextNotEmptyValidator(wx.PyValidator):
    def __init__(self, error_label):
        wx.PyValidator.__init__(self)
        self.error_label = error_label

    def Clone(self):
        return TextNotEmptyValidator(self.error_label)

    def Validate(self, win):
        textCtrl = self.GetWindow()
        text = textCtrl.GetValue()

        if not text:
            self.error_label.SetLabel('validation fail')
            #wx.MessageBox('validator error', 'Error')
            textCtrl.SetFocus()
            textCtrl.GetParent().Refresh()
            return False
        else:
            self.error_label.SetLabel('')
            return True

    def TransferToWindow(self):
        return True

    def TransferFromWindow(self):
        return True
