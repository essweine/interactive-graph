from math import ceil
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
            group.build(self._ax, offset_x + row_sz / 2.0, offset_x + row_sz * 1.2, offset_y, radius, font_size)

        self._ax.tick_params(left = False, bottom = False, labelleft = False, labelbottom = False)
        self._ax.set_ylim(1.0 - row_sz * n_rows)
        self._ax.set_aspect("equal")
        self._ax.set_anchor("NW")
        self._ax.figure.canvas.toolbar.update()

    def update(self, action):

        for group in self._groups:
            if action == "hide":
                if group.selected:
                    group.mark_hidden()
            elif action == "restore":
                if group.selected:
                    group.mark_visible()
            elif action == "deselect":
                if group.selected:
                    group.mark_unselected()
            elif action == "reset":
                group.mark_visible()

        self.ax.figure.canvas.draw()

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

        self._selected = False
        self._visible = True

        self._patch = None
        self._text = None

    def build(self, ax, circle_x, text_x, y, radius, font_size):

        self._default_props["radius"] = radius
        self._selected_props["radius"] = radius
        self._patch = plt.Circle((circle_x, y), **self.default_props)
        ax.add_patch(self._patch)
        self._text = ax.text(text_x, y, self.label, va = "center", ha = "left", size = font_size)
        self._connect()

    @property
    def label(self):
        return self._label

    @property
    def selected(self):
        return self._selected

    @property
    def visible(self):
        return self._visible

    @property
    def default_props(self):
        return self._default_props

    @property
    def selected_props(self):
        return self._selected_props

    def mark_selected(self):

        mplartist.setp(self._patch, **self.selected_props)
        self._selected = True

    def mark_unselected(self):

        mplartist.setp(self._patch, **self.default_props)
        self._selected = False

    def mark_visible(self):

        self._text.set_color((0.0, 0.0, 0.0))
        self._visible = True

    def mark_hidden(self):

        self._text.set_color((0.4, 0.4, 0.4))
        self._visible = False

    def _on_press(self, event):

        if event.inaxes != self._patch.axes:
            return
        contains, attrd = self._patch.contains(event)
        if not contains:
            return

        if self._selected:
            self._legend._selection.remove_vertices(self._vertices)
            self.mark_unselected()
        else:
            self._legend._selection.add_vertices(self._vertices)
            self.mark_selected()

        self._legend.ax.figure.canvas.draw()

    def _connect(self):

        self._cidpress = self._patch.figure.canvas.mpl_connect("button_press_event", self._on_press)

    def _disconnect(self):

        self._patch.figure.canvas.mpl_disconnect(self._cidpress)

