from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg as NavigationToolbar
from matplotlib.backends.backend_wx import _load_bitmap
import wx
import platform
from worldstate import WorldState
from large_plot import LargePlotDialog
import wx.lib.agw.pycollapsiblepane as PCP
import os


class BioPepaToolbar(NavigationToolbar):

    ON_CUSTOM_ENLARGE = wx.NewId()
    ANNOTATE_ARROW = wx.NewId()
    ANNOTATE_TEXT = wx.NewId()
    ANNOTATE_TEXT_ARROW = wx.NewId()
    ANNOTATE_CIRCLE = wx.NewId()

    if (platform.system() != "Linux"):
        #None is for the separators
        toolitems = [t for t in NavigationToolbar.toolitems if t[0] in ('Home', 'Pan', 'Zoom', 'Back', 'Forward', None)]

    def __init__(self, graph_canvas):
        super(BioPepaToolbar, self).__init__(graph_canvas)
        cwd = os.getcwd()
        self.world = WorldState.Instance()
        if (platform.system() == "Linux"):
            #save
            self.DeleteToolByPos(8)
            #subplots
            self.DeleteToolByPos(7)

        self.AddSimpleTool(self.ON_CUSTOM_ENLARGE, _load_bitmap(cwd + '/icons/full_screen.xpm'), 'Enlarge Graph', 'Enlarge Graph')
        wx.EVT_TOOL(self, self.ON_CUSTOM_ENLARGE, self._on_custom_enlarge)

        self.AddSimpleTool(self.ANNOTATE_ARROW, _load_bitmap(cwd + '/icons/arrow.xpm'), 'Annotate with an Arrow', 'Annotate with an Arrow')
        wx.EVT_TOOL(self, self.ANNOTATE_ARROW, self._on_custom_annotate_arrow)

        self.AddSimpleTool(self.ANNOTATE_TEXT, _load_bitmap(cwd + '/icons/text.xpm'), 'Annotate with Text', 'Annotate with Text')
        wx.EVT_TOOL(self, self.ANNOTATE_TEXT, self._on_custom_annotate_text)

        self.AddSimpleTool(self.ANNOTATE_TEXT_ARROW, _load_bitmap(cwd + '/icons/text_arrow.xpm'), 'Annotate with an Arrow and Text', 'Annotate with an Arrow and Text')
        wx.EVT_TOOL(self, self.ANNOTATE_TEXT_ARROW, self._on_custom_annotate_text_arrow)

        self.AddSimpleTool(self.ANNOTATE_CIRCLE, _load_bitmap(cwd + '/icons/circle.xpm'), 'Annotate with a circle', 'Annotate with a circle')
        wx.EVT_TOOL(self, self.ANNOTATE_CIRCLE, self._on_custom_annotate_circle)

    def _on_custom_enlarge(self, e):
        large_plot = LargePlotDialog(None, title='Big Plot')
        large_plot.ShowModal()
        large_plot.Destroy()

    def _on_custom_annotate_arrow(self, e):
        self.world.annotate = not self.world.annotate
        self.world.annotation_mode = self.world._ARROW

    def _on_custom_annotate_text(self, e):
        self.world.annotate = not self.world.annotate
        self.world.annotation_mode = self.world._TEXT

    def _on_custom_annotate_text_arrow(self, e):
        self.world.annotate = not self.world.annotate
        self.world.annotation_mode = self.world._TEXT_ARROW

    def _on_custom_annotate_circle(self, e):
        self.world.annotate = not self.world.annotate
        self.world.annotation_mode = self.world._CIRCLE

if (platform.system() == "Linux"):
    class BioPepaCollapsiblePane(PCP.PyCollapsiblePane):
        def __init__(self, legend_panel, result):
            super(BioPepaCollapsiblePane, self).__init__(legend_panel, wx.ID_ANY, result)
else:
    class BioPepaCollapsiblePane(wx.CollapsiblePane):
        def __init__(self, legend_panel, result):
            super(BioPepaCollapsiblePane, self).__init__(legend_panel, wx.ID_ANY, result)
