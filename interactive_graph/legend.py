from math import ceil
from copy import deepcopy
import matplotlib.pyplot as plt
import matplotlib.artist as mplartist
from matplotlib.axes import Axes

class InteractiveLegend(object):

    def __init__(self, graph, selection):

        self._graph = graph
        self._selection = selection
        self._groups = [ ]
        self._ax = Axes(self._graph.ax.get_figure(), self._graph.ax.get_position(original = True))

        # TODO: accept groups as part of constructor?

    def add_group(self, label, vertices, default_props = { }, selected_props = { }, position = None):

        group = VertexGroup(self, label, vertices, default_props, selected_props)
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
            group._radius = radius
            group._patch = plt.Circle((offset_x + row_sz / 2.0, offset_y), **group.default_patch_props)
            self._ax.add_patch(group._patch)
            self._ax.text(offset_x + row_sz * 1.2, offset_y, group.label, va = "center", ha = "left", size = font_size)
            group._connect()

        self._ax.tick_params(left = False, bottom = False, labelleft = False, labelbottom = False)
        self._ax.set_ylim(1.0 - row_sz * n_rows)
        self._ax.set_aspect("equal")
        self._ax.set_anchor("NW")

    def _select(self, vertices):

        self._selection.add_vertices(vertices)

    def _deselect(self, vertices):

        self._selection.remove_vertices(vertices)

    def reset(self):

        for group in self._groups:
            if group.selected:
                group.reset_props()

    @property
    def ax(self):
        return self._ax

class VertexGroup(object):

    def __init__(self, legend, label, vertices, default_props, selected_props):
        
        self._legend = legend
        self._label = label
        self._vertices = vertices
        self._default_props = default_props
        self._selected_props = selected_props

        self._radius = 0.1
        self._patch = None
        self._selected = False

    @property
    def label(self):
        return self._label

    @property
    def selected(self):
        return self._selected

    @property
    def default_patch_props(self):
        props = deepcopy(self.default_vertex_props)
        props["radius"] = self._radius
        return props

    @property
    def selected_patch_props(self):
        props = deepcopy(self.selected_vertex_props)
        props["radius"] = self._radius
        return props

    @property
    def default_vertex_props(self):
        return self._default_props

    @property
    def selected_vertex_props(self):
        return self._selected_props

    def reset_props(self):

        mplartist.setp(self._patch, **self.default_patch_props)
        self._patch.figure.canvas.draw()
        self._selected = False

    def _on_press(self, event):

        if event.inaxes != self._patch.axes:
            return

        contains, attrd = self._patch.contains(event)
        if not contains:
            return

        if self._selected:
            self._legend._deselect(self._vertices)
            mplartist.setp(self._patch, **self.default_patch_props)
            self._patch.figure.canvas.draw()
            self._selected = False
        else:
            self._legend._select(self._vertices)
            mplartist.setp(self._patch, **self.selected_patch_props)
            self._patch.figure.canvas.draw()
            self._selected = True

    def _connect(self):

        self._cidpress = self._patch.figure.canvas.mpl_connect("button_press_event", self._on_press)

    def _disconnect(self):

        self._patch.figure.canvas.mpl_disconnect(self._cidpress)

