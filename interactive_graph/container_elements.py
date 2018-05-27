import matplotlib.pyplot as plt
from matplotlib.axes import Axes

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

