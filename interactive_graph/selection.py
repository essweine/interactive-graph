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

    def __init__(self, selection, font_size = 10, pad = 6):

        self._selection = selection
        self._ax = Axes(selection._graph.ax.get_figure(), selection._graph.ax.get_position(original = True))

        button_sz = 1.0 / (self._ax.figure.get_dpi() / (font_size + pad))
        pad_sz = 0.02
        labels = [ "deselect all", "toggle complement", "toggle selection" ]
        props = { "fc": (0.95, 0.95, 0.95), "ec": (0.1, 0.1, 0.1) }
        buttons = [ plt.Rectangle((0.0, i * (button_sz + pad_sz)), 1.0, button_sz, **props) for i in range(3) ]
        text_offsets = [ i * (button_sz + pad_sz) + (0.5 * button_sz) for i in range(3) ]
        for button, offset, label in zip(buttons, text_offsets, labels):
            self._ax.add_patch(button)
            self._ax.text(0.5, offset, label, size = font_size, ha = "center", va = "center")

        self._ax.tick_params(left = False, labelleft = False, bottom = False, labelbottom = False)
        self._ax.set_frame_on(False)
        self._ax.set_anchor("NW")
        self._ax.set_ylim(0, 3 * button_sz + 2 * pad_sz)

    @property
    def ax(self):
        return self._ax
