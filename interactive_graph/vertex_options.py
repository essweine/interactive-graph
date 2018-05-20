import matplotlib.pyplot as plt
from matplotlib.axes import Axes

from container import Toggle, Option

class VertexOptions(object):

    def __init__(self, graph, font_sz = 8, pad = 4):

        self._graph = graph
        self._ax = Axes(graph.ax.get_figure(), graph.ax.get_position(original = True))

        button_sz = 1.0 / (self._ax.figure.get_dpi() / (font_sz + pad))
        n_rows, pad_sz = len(graph.press_actions), 0.02
        rows = [ i * (button_sz + pad_sz) for i in range(n_rows) ]

        self._actions = { }
        for name, row in zip(graph.press_actions, rows):
            action = self._set_action(name)
            self._actions[name] = Toggle(self._ax, (0.0, row), 1.0, button_sz, font_sz, action, name)

        current = graph._press_action
        self._actions[current]._set_pressed()

        self._ax.tick_params(left = False, labelleft = False, bottom = False, labelbottom = False)
        self._ax.set_frame_on(False)
        self._ax.set_anchor("NW")
        self._ax.set_ylim(0, n_rows * button_sz + (n_rows - 1) * pad_sz)

    def _set_action(self, name):

        def action(toggled):
            self._graph.set_press_action(name)
            for act in self._actions:
                if act != name:
                    self._actions[act]._set_unpressed()

        return action

    @property
    def ax(self):
        return self._ax


