import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable, Size
from matplotlib.axes import Axes
from math import ceil

class GraphContainer(object):

    def __init__(self, ax, graph, legend, select_opts):

        self._ax = ax

        self._graph = graph
        self._legend = legend
        self._select_opts = select_opts

        pad = Size.Fixed(0.1)
        graph_width = Size.AxesX(graph.ax)
        self.menu_width = Size.Fraction(0.35, Size.AxesX(graph.ax))
        self.n_rows = 12
        self.cell_height = Size.Fraction(0.98 / 10.0, Size.AxesY(graph.ax))

        divider = make_axes_locatable(ax)
        divider.set_horizontal([ graph_width, pad, self.menu_width ])

        leg_span = self._get_span(legend.ax)
        leg_top, leg_bottom = self.n_rows, self.n_rows - leg_span
        menu_layout = [ self.cell_height ] * leg_span + [ pad ]

        sel_opts_span = self._get_span(select_opts.ax)
        sel_opts_top, sel_opts_bottom = leg_bottom - 1, leg_bottom - sel_opts_span - 1
        menu_layout += [ self.cell_height ] * sel_opts_span + [ pad ]

        # Placeholder for unimplemented menu items
        menu_layout += [ self.cell_height ] * (sel_opts_bottom - 1)

        divider.set_vertical([ c for c in reversed(menu_layout) ])
        self.divider = divider

        graph.ax.set_axes_locator(divider.new_locator(nx = 0, ny = 0, ny1 = -1))
        ax.figure.add_axes(graph.ax)

        legend.ax.set_axes_locator(divider.new_locator(nx = 2, ny = leg_bottom, ny1 = leg_top))
        ax.figure.add_axes(legend.ax)

        select_opts.ax.set_axes_locator(divider.new_locator(nx = 2, ny = sel_opts_bottom, ny1 = sel_opts_top))
        ax.figure.add_axes(select_opts.ax)

        ax.set_axes_locator(divider.new_locator(nx = 2, ny = 0, ny1 = sel_opts_bottom - 1))
        ax.tick_params(left = False, labelleft = False, bottom = False, labelbottom = False)

    def _get_span(self, ax):

        bottom, top = ax.get_ylim()
        height = top - bottom
        scaled = height * self.menu_width.get_size(self._ax)[0]
        n_rows = ceil(scaled / self.cell_height.get_size(self._ax)[0])
        return int(n_rows)

