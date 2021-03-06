import wx

"""
Validators for the wizard
"""


class TextNotEmptyValidator(wx.PyValidator):
    """
    Have we entered a title?
    error label is a wx.StaticText on the wizard page
    """
    def __init__(self, error_label):
        wx.PyValidator.__init__(self)
        self.error_label = error_label

    def Clone(self):
        return TextNotEmptyValidator(self.error_label)

    def Validate(self, win):
        textCtrl = self.GetWindow()
        text = textCtrl.GetValue()

        if not text:
            self.error_label.SetLabel('***Please enter a title***')
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


class ResultsListNotEmptyValidator(wx.PyValidator):
    """
    Have we selected a results file?
    """
    def __init__(self, error_label):
        wx.PyValidator.__init__(self)
        self.error_label = error_label

    def Clone(self):
        return ResultsListNotEmptyValidator(self.error_label)

    def Validate(self, win):
        results_list = self.GetWindow()
        results_count = results_list.GetCount()

        if not results_count:
            self.error_label.SetLabel('***Please select at least one results file***')
            results_list.SetFocus()
            results_list.GetParent().Refresh()
            return False
        else:
            self.error_label.SetLabel('')
            return True

    def TransferToWindow(self):
        return True

    def TransferFromWindow(self):
        return True
