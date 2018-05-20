import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable, Size
from matplotlib.axes import Axes
from math import ceil

class GraphContainer(object):

    def __init__(self, ax, graph, legend, select_opts, vertex_opts):

        self._ax = ax

        self._graph = graph
        self._legend = legend
        self._select_opts = select_opts
        self._vertex_opts = vertex_opts

        pad = Size.Fixed(0.1)
        graph_width = Size.AxesX(graph.ax)
        self.menu_width = Size.Fraction(0.35, Size.AxesX(graph.ax))
        self.n_rows = 13
        self.cell_height = Size.Fraction(0.97 / 10.0, Size.AxesY(graph.ax))

        divider = make_axes_locatable(ax)
        divider.set_horizontal([ graph_width, pad, self.menu_width ])

        leg_span = self._get_span(legend.ax)
        leg_top, leg_bottom = self.n_rows, self.n_rows - leg_span
        menu_layout = [ self.cell_height ] * leg_span + [ pad ]

        sel_opts_span = self._get_span(select_opts.ax)
        sel_opts_top, sel_opts_bottom = leg_bottom - 1, leg_bottom - sel_opts_span - 1
        menu_layout += [ self.cell_height ] * sel_opts_span + [ pad ]

        vx_opts_span = self._get_span(vertex_opts.ax)
        vx_opts_top, vx_opts_bottom = sel_opts_bottom - 1, sel_opts_bottom - vx_opts_span - 1
        menu_layout += [ self.cell_height ] * vx_opts_span + [ pad ]

        # Placeholder for unimplemented menu items
        menu_layout += [ self.cell_height ] * (vx_opts_bottom - 1)

        divider.set_vertical([ c for c in reversed(menu_layout) ])
        self.divider = divider

        graph.ax.set_axes_locator(divider.new_locator(nx = 0, ny = 0, ny1 = -1))
        ax.figure.add_axes(graph.ax)

        legend.ax.set_axes_locator(divider.new_locator(nx = 2, ny = leg_bottom, ny1 = leg_top))
        ax.figure.add_axes(legend.ax)

        select_opts.ax.set_axes_locator(divider.new_locator(nx = 2, ny = sel_opts_bottom, ny1 = sel_opts_top))
        ax.figure.add_axes(select_opts.ax)

        vertex_opts.ax.set_axes_locator(divider.new_locator(nx = 2, ny = vx_opts_bottom, ny1 = vx_opts_top))
        ax.figure.add_axes(vertex_opts.ax)

        ax.set_axes_locator(divider.new_locator(nx = 2, ny = 0, ny1 = vx_opts_bottom - 1))
        ax.tick_params(left = False, labelleft = False, bottom = False, labelbottom = False)

    def _get_span(self, ax):

        bottom, top = ax.get_ylim()
        height = top - bottom
        scaled = height * self.menu_width.get_size(self._ax)[0]
        n_rows = ceil(scaled / self.cell_height.get_size(self._ax)[0])
        return int(n_rows)

class Option(object):

    unclicked_props = { "fc": (0.95, 0.95, 0.95), "ec": (0.1, 0.1, 0.1) }
    clicked_props = { "fc": (0.85, 0.85, 0.85), "ec": (0.1, 0.1, 0.1) }

    def __init__(self, ax, loc, width, height, font_sz, label, action):

        self.button = plt.Rectangle(loc, width, height, **Option.unclicked_props)
        ax.add_patch(self.button)
        x, y = loc[0] + width / 2.0, loc[1] + height / 2.0
        self.text = ax.text(x, y, label, size = font_sz, ha = "center", va = "center")
        self._connect()

        self._press_action = action

    def _on_press(self, event):

        if event.inaxes != self.button.axes:
            return
        contains, attrd = self.button.contains(event)
        if not contains:
            return

        self._press_action()
        self.button.figure.canvas.draw()

    def _connect(self):

        self._cidpress = self.button.figure.canvas.mpl_connect("button_press_event", self._on_press)

    def _disconnect(self):

        self.button.figure.canvas.mpl_disconnect(self._cidpress)

class Toggle(Option):

    def __init__(self, ax, loc, width, height, font_sz, action,
                 unclicked_label, clicked_label = None):

        self.unclicked_label = unclicked_label
        if clicked_label is not None:
            self.clicked_label = clicked_label
        else:
            self.clicked_label = unclicked_label

        super(Toggle, self).__init__(ax, loc, width, height, font_sz, unclicked_label, self.toggle)

        self.action = action
        self.pressed = False

    def _set_pressed(self):

        self.button.set(**Option.clicked_props)
        self.text.set_text(self.clicked_label)
        self.pressed = True

    def _set_unpressed(self):

        self.button.set(**Option.unclicked_props)
        self.text.set_text(self.unclicked_label)
        self.pressed = False

    def toggle(self):

        if self.pressed is True:
            self._set_unpressed()
            self.action(False)
        else:
            self._set_pressed()
            self.action(True)

