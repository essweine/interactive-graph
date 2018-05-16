from exceptions import NonexistentVertexError

import matplotlib.pyplot as plt
from matplotlib.axes import Axes

class Selection(object):

    def __init__(self, graph, props = { }):

        self._graph = graph
        self._selected = set()
        self._selected_props = props
        self._complement = set()      # Only needed for restoring state after hiding complement

    def select_or_deselect(self, vxid):

        if vxid in self._selected:
            self._selected.remove(vxid)
            self._graph.restore_vertex_props(vxid)
        else:
            self._selected.add(vxid)
            self._graph.update_vertex_props(vxid, **self._selected_props)

    def hide_selection(self):

        self._graph.hide_vertices(self._selected & self._graph.visible_vertices)

    def restore_selection(self):

        self._graph.restore_vertices(self._selected & self._graph.hidden_vertices)

    def hide_complement(self):

        self._complement = self._graph.visible_vertices - self._selected
        self._graph.hide_vertices(self._graph.visible_vertices - self._selected)

    def restore_complement(self):

        self._graph.restore_vertices(self._complement & self._graph.hidden_vertices)
        self._complement.clear()

    def deselect_all(self):

        self._graph.restore_vertices_props(self._selected)
        self._selected.clear()
        self._complement.clear()

    def add_vertices(self, vertices):

        self._selected |= vertices
        self._complement.clear()
        if self.selected_props:
            self._graph.update_vertices_props(vertices, **self.selected_props)

    def remove_vertices(self, vertices):

        self._selected -= vertices
        self._complement.clear()
        self._graph.restore_vertices_props(vertices)

    def get_selection(self):

        return self._selected

    @property
    def selected_props(self):
        return self._selected_props

class SelectionOptions(object):

    def __init__(self, selection, font_sz = 10, pad = 6, legend = None):

        self._selection = selection
        self._legend = legend
        self._ax = Axes(selection._graph.ax.get_figure(), selection._graph.ax.get_position(original = True))

        button_sz = 1.0 / (self._ax.figure.get_dpi() / (font_sz + pad))
        pad_sz = 0.02
        rows = [ i * (button_sz + pad_sz) for i in range(3) ]

        self.actions = {
            "hide": Option("hide selection", self._hide_selection, self._ax, (0.0, rows[2]), 0.49, button_sz, font_sz, None),
            "restore": Option("restore selection", self._restore_selection, self._ax, (0.51, rows[2]), 0.49, button_sz, font_sz, None),
            "complement": Option("complement", self._toggle_complement, self._ax, (0.0, rows[1]), 1.0, button_sz, font_sz),
            "deselect": Option("deselect all", self._deselect_all, self._ax, (0.0, rows[0]), 1.0, button_sz, font_sz, None),
        }

        self._ax.tick_params(left = False, labelleft = False, bottom = False, labelbottom = False)
        self._ax.set_frame_on(False)
        self._ax.set_anchor("NW")
        self._ax.set_ylim(0, 3 * button_sz + 2 * pad_sz)

    def _toggle_complement(self, visible):

        if visible:
            self._selection.hide_complement()
        else:
            self._selection.restore_complement()

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

    @property
    def ax(self):
        return self._ax

class Option(object):

    unclicked_props = { "fc": (0.95, 0.95, 0.95), "ec": (0.1, 0.1, 0.1) }
    clicked_props = { "fc": (0.90, 0.90, 0.90), "ec": (0.1, 0.1, 0.1) }

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

    def _on_press(self, event):

        if event.inaxes != self.button.axes:
            return
        contains, attrd = self.button.contains(event)
        if not contains:
            return

        if self.toggle is None:
            self.action()
        elif self.toggle is True:
            self.button.set(**Option.clicked_props)
            self.text.set_text("restore %s" % self.label)
            self.action(self.toggle)
            self.toggle = False
        else:
            self.button.set(**Option.unclicked_props)
            self.text.set_text("hide %s" % self.label)
            self.action(self.toggle)
            self.toggle = True

    def _connect(self):

        self._cidpress = self.button.figure.canvas.mpl_connect("button_press_event", self._on_press)

    def _disconnect(self):

        self.button.figure.canvas.mpl_disconnect(self._cidpress)
