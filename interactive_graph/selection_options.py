import matplotlib.pyplot as plt
from matplotlib.axes import Axes

class SelectionOptions(object):

    def __init__(self, selection, font_sz = 8, pad = 4, legend = None):

        self._selection = selection
        self._legend = legend
        self._ax = Axes(selection._graph.ax.get_figure(), selection._graph.ax.get_position(original = True))

        button_sz = 1.0 / (self._ax.figure.get_dpi() / (font_sz + pad))
        n_rows, pad_sz = 4, 0.02
        rows = [ i * (button_sz + pad_sz) for i in range(n_rows) ]

        self._actions = {
            "hide": Option("hide selection", self._hide_selection, self._ax, (0.0, rows[3]), 0.49, button_sz, font_sz, None),
            "restore": Option("restore selection", self._restore_selection, self._ax, (0.51, rows[3]), 0.49, button_sz, font_sz, None),
            "deselect": Option("deselect all", self._deselect_all, self._ax, (0.0, rows[2]), 0.49, button_sz, font_sz, None),
            "reset": Option("restore all", self._restore_all, self._ax, (0.51, rows[2]), 0.49, button_sz, font_sz, None),
            "in": Option("in neighbors", self._toggle_in_neighbors, self._ax, (0.0, rows[1]), 0.49, button_sz, font_sz),
            "out": Option("out neighbors", self._toggle_out_neighbors, self._ax, (0.51, rows[1]), 0.49, button_sz, font_sz),
            "complement": Option("others", self._toggle_complement, self._ax, (0.0, rows[0]), 1.0, button_sz, font_sz),
        }

        self._ax.tick_params(left = False, labelleft = False, bottom = False, labelbottom = False)
        self._ax.set_frame_on(False)
        self._ax.set_anchor("NW")
        self._ax.set_ylim(0, n_rows * button_sz + (n_rows - 1) * pad_sz)

    def _toggle_complement(self, visible):

        if visible:
            self._selection.hide_complement()
            self._actions["in"]._set_pressed()
            self._actions["out"]._set_pressed()
        else:
            self._selection.restore_complement()
            self._actions["in"]._set_unpressed()
            self._actions["out"]._set_unpressed()

    def _toggle_in_neighbors(self, visible):

        if visible:
            self._selection.hide_in_neighbors()
        else:
            self._selection.restore_in_neighbors()

    def _toggle_out_neighbors(self, visible):

        if visible:
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

class Option(object):

    unclicked_props = { "fc": (0.95, 0.95, 0.95), "ec": (0.1, 0.1, 0.1) }
    clicked_props = { "fc": (0.85, 0.85, 0.85), "ec": (0.1, 0.1, 0.1) }

    def __init__(self, label, action, ax, loc, width, height, font_sz, toggle = True):

        self.toggle = toggle    # True when items visible; False when items hidden; None if not a toggle
        self.label = label
        self.action = action

        self.button = plt.Rectangle(loc, width, height, **Option.unclicked_props)
        ax.add_patch(self.button)
        x, y = loc[0] + width / 2.0, loc[1] + height / 2.0
        if toggle is True:
            self.text = ax.text(x, y, "hide %s" % label, size = font_sz, ha = "center", va = "center")
        else:
            self.text = ax.text(x, y, "%s" % label, size = font_sz, ha = "center", va = "center")
        self._connect()

    def _set_pressed(self):

        self.button.set(**Option.clicked_props)
        self.text.set_text("restore %s" % self.label)
        self.toggle = False

    def _set_unpressed(self):

        self.button.set(**Option.unclicked_props)
        self.text.set_text("hide %s" % self.label)
        self.toggle = True

    def _on_press(self, event):

        if event.inaxes != self.button.axes:
            return
        contains, attrd = self.button.contains(event)
        if not contains:
            return

        if self.toggle is None:
            self.action()
        elif self.toggle is True:
            self.action(self.toggle)
            self._set_pressed()
        else:
            self.action(self.toggle)
            self._set_unpressed()

        self.button.figure.canvas.draw()

    def _connect(self):

        self._cidpress = self.button.figure.canvas.mpl_connect("button_press_event", self._on_press)

    def _disconnect(self):

        self.button.figure.canvas.mpl_disconnect(self._cidpress)
