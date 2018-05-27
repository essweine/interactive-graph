import matplotlib.pyplot as plt
from matplotlib.axes import Axes

from container_elements import Toggle, Option
from legend import InteractiveLegend

class SelectionOptions(object):

    def __init__(self, selection, font_sz = 8, pad = 4, legend = None):

        self._selection = selection
        self._ax = Axes(selection._graph.ax.get_figure(), selection._graph.ax.get_position(original = True))

        self._legend = legend

        button_sz = 1.0 / (self._ax.figure.get_dpi() / (font_sz + pad))
        n_rows, pad_sz = 5, 0.02
        rows = [ i * (button_sz + pad_sz) for i in range(n_rows) ]

        self._actions = {
            "hide": Option(self._ax, (0.0, rows[4]), 0.49, button_sz, font_sz, "hide selection", self._hide_selection),
            "restore": Option(self._ax, (0.51, rows[4]), 0.49, button_sz, font_sz, "restore selection", self._restore_selection),
            "in": Toggle(self._ax, (0.0, rows[3]), 0.49, button_sz, font_sz, self._toggle_in_neighbors, "hide in neighbors", "restore in neighbors"),
            "out": Toggle(self._ax, (0.51, rows[3]), 0.49, button_sz, font_sz, self._toggle_out_neighbors, "hide out neighbors", "restore out neighbors"),
            "complement": Toggle(self._ax, (0.0, rows[2]), 1.0, button_sz, font_sz, self._toggle_complement, "hide others", "restore others"),
            "remove": Option(self._ax, (0.0, rows[1]), 1.0, button_sz, font_sz, "remove selection", self._remove_selection),
            "deselect": Option(self._ax, (0.0, rows[0]), 1.0, button_sz, font_sz, "deselect all", self._deselect_all),
        }

        self._ax.tick_params(left = False, labelleft = False, bottom = False, labelbottom = False)
        self._ax.set_frame_on(False)
        self._ax.set_anchor("NW")
        self._ax.set_ylim(0, n_rows * button_sz + (n_rows - 1) * pad_sz)

    def create_legend(self):

        self._legend = InteractiveLegend(self._selection._graph, self._selection)
        return self._legend

    @property
    def has_legend(self):
        return self._legend is not None

    def _toggle_complement(self, toggled):

        if toggled:
            self._selection.hide_complement()
            self._actions["in"]._set_pressed()
            self._actions["out"]._set_pressed()
        else:
            self._selection.restore_complement()
            self._actions["in"]._set_unpressed()
            self._actions["out"]._set_unpressed()

    def _toggle_in_neighbors(self, toggled):

        if toggled:
            self._selection.hide_in_neighbors()
        else:
            self._selection.restore_in_neighbors()

    def _toggle_out_neighbors(self, toggled):

        if toggled:
            self._selection.hide_out_neighbors()
        else:
            self._selection.restore_out_neighbors()

    def _hide_selection(self):

        if self._legend is not None:
            self._legend.update("hide")
        self._selection.hide_selection()

    def _restore_selection(self):

        if self._legend is not None:
            self._legend.update("restore")
        self._selection.restore_selection()

    def _remove_selection(self):

        self._selection.remove_selection()
        if self._legend is not None:
            self._legend.update("remove")

    def _deselect_all(self):

        if self._legend is not None:
            self._legend.update("deselect")
        self._selection.deselect_all()

    def _restore_all(self):

        if self._legend is not None:
            self._legend.update("reset")
        self._actions["in"]._set_unpressed()
        self._actions["out"]._set_unpressed()
        self._actions["complement"]._set_unpressed()
        self._selection._graph.restore_all()

    @property
    def ax(self):
        return self._ax


