from math import ceil
from copy import deepcopy
import matplotlib.pyplot as plt
from matplotlib.axes import Axes

class InteractiveLegend(object):

    def __init__(self, graph, selection):

        self._graph = graph
        self._selection = selection
        self._groups = [ ]
        self._ax = Axes(self._graph.ax.get_figure(), self._graph.ax.get_position(original = True))

    def add_group(self, label, vertices, default_props = { }, selected_props = { }, position = None):

        group = VertexGroup(label, vertices, default_props, selected_props)
        if position is None:
            self._groups.append(group)
        else:
            self._groups.insert(position, group)

    def build(self, n_cols = 2, font_size = 8, pad = 4):

        n_rows = int(ceil(len(self._groups) / float(n_cols)))
        row_sz = 1.0 / (self._ax.figure.get_dpi() / (font_size + pad))
        radius = row_sz * 0.8 / 2.0

        for idx, group in enumerate(self._groups):
            row, col = idx % n_rows, idx // n_rows
            offset_y = 1.0 - (row_sz * row + row_sz / 2.0)
            offset_x = (1.0 / n_cols) * col
            props = deepcopy(group.default_props)
            props["radius"] = radius
            c = plt.Circle((offset_x + row_sz / 2.0, offset_y), **props)
            self._ax.add_patch(c)
            self._ax.text(offset_x + row_sz * 1.2, offset_y, group.label, va = "center", ha = "left", size = font_size)

        self._ax.tick_params(left = False, bottom = False, labelleft = False, labelbottom = False)
        self._ax.set_ylim(1.0 - row_sz * n_rows)
        self._ax.set_aspect("equal")
        self._ax.set_anchor("NW")

class VertexGroup(object):

    def __init__(self, label, vertices, default_props, selected_props):
        
        self._label = label
        self._vertices = vertices
        self._default_props = default_props
        self._selected_props = selected_props

    @property
    def label(self):
        return self._label

    @property
    def default_props(self):
        return self._default_props

    @property
    def selected_props(self):
        return self._selected_props
