class Vertex(object):

    lock = None
    annotation_props = dict(boxstyle = "square", fc = (0.2, 0.2, 0.2, 0.6), ec = (0.2, 0.2, 0.2, 0.8))

    def __init__(self, vertex_id, graph, circle, label = ""):

        self.vertex_id = vertex_id
        self.graph = graph
        self.circle = circle
        x, y = circle.center
        self.annotation = self.circle.axes.text(x, y, label, bbox = Vertex.annotation_props, visible = False)

        self._in_edges = set()
        self._out_edges = set()
        self._loops = set()

        self._hidden_in_edges = set()
        self._hidden_out_edges = set()
        self._hidden_loops = set()

        self.press = None
        self.background = None

    def hide(self):

        self._hidden_in_edges |= self._in_edges
        self._hidden_out_edges |= self._out_edges
        self._hidden_loops |= self._loops

        self._in_edges.clear()
        self._out_edges.clear()
        self._loops.clear()

        if self.annotation.get_visible() is True:
            self.annotation.set_visible(False)
        self.circle.remove()

    def restore(self, ax, in_edges, out_edges):

        self._in_edges |= in_edges
        self._out_edges |= out_edges
        self._loops |= self._hidden_loops

        self._hidden_in_edges -= in_edges
        self._hidden_out_edges -= out_edges
        self._hidden_loops.clear()

        self.circle.set_figure(ax.figure)
        ax.add_artist(self.circle)

    def remove(self):

        self.annotation.remove()
        self.circle.remove()

    def update_circle(self, new, ax):

        self.disconnect()
        self.circle.remove()
        new.center = self.circle.center
        new.set_figure(ax.figure)
        ax.add_artist(new)
        self.circle = new
        for edge in self.in_edges | self.out_edges:
            artist = self.graph.get_edge(edge)
            artist.update()
        self.connect()

    def on_press(self, event):

        if event.inaxes != self.circle.axes:
            return

        contains, attrd = self.circle.contains(event)
        if not contains:
            return

        if self.graph.press_action == "move":
            self.move(event)
        elif self.graph.press_action == "hide":
            self.graph.hide_vertex(self.vertex_id)
        elif self.graph.press_action == "remove":
            self.graph.hide_vertex(self.vertex_id)
        elif self.graph.press_action == "expand":
            self.graph.expand_or_collapse(self.vertex_id)

    def move(self, event):

        if Vertex.lock is not None:
            return

        Vertex.lock = self

        if self.annotation.get_visible() is True:
            self.annotation.set_visible(False)

        x0, y0 = event.xdata, event.ydata
        self.press = x0, y0, event.xdata, event.ydata

        canvas = self.circle.figure.canvas
        axes = self.circle.axes
        self.circle.set_animated(True)
        canvas.draw()
        self.background = canvas.copy_from_bbox(self.circle.axes.bbox)
        axes.draw_artist(self.circle)
        canvas.blit(axes.bbox)

    def on_motion(self, event):

        if event.inaxes != self.circle.axes:
            return

        contains, attrd = self.circle.contains(event)
        if not contains and self.annotation.get_visible() is True:
            self.annotation.set_visible(False)
            self.annotation.figure.canvas.draw()
        if contains and self.press is None:
            self.annotation.set_visible(True)
            self.annotation.figure.canvas.draw()

        if self.press is None:
            return

        if Vertex.lock is not self:
            return

        x0, y0, xpress, ypress = self.press
        dx, dy = event.xdata - xpress, event.ydata - ypress
        self.circle.center = (x0 + dx, y0 + dy)

        for edge in self._in_edges | self._out_edges:
            artist = self.graph.get_edge(edge)
            artist.update()

        canvas = self.circle.figure.canvas
        axes = self.circle.axes
        canvas.restore_region(self.background)
        axes.draw_artist(self.circle)
        canvas.blit(axes.bbox)

    def on_release(self, event):

        if Vertex.lock is not self:
            return

        for edge in self._in_edges | self._out_edges:
            artist = self.graph.get_edge(edge)
            artist.update()

        self.press = None
        Vertex.lock = None
        self.circle.set_animated(False)
        self.background = None
        self.circle.figure.canvas.draw()

        x, y = self.circle.center
        self.annotation.set_x(x), self.annotation.set_y(y)

    def connect(self):

        self.cidpress = self.circle.figure.canvas.mpl_connect("button_press_event", self.on_press)
        self.cidrelease = self.circle.figure.canvas.mpl_connect("button_release_event", self.on_release)
        self.cidmotion = self.circle.figure.canvas.mpl_connect("motion_notify_event", self.on_motion)

    def disconnect(self):

        self.circle.figure.canvas.mpl_disconnect(self.cidpress)
        self.circle.figure.canvas.mpl_disconnect(self.cidrelease)
        self.circle.figure.canvas.mpl_disconnect(self.cidmotion)

    @property
    def in_edges(self):
        return self._in_edges | self._hidden_in_edges

    @property
    def out_edges(self):
        return self._out_edges | self._hidden_out_edges

    @property
    def loops(self):
        return self._loops | self._hidden_loops

    @property
    def visible_in_edges(self):
        return self._in_edges

    @property
    def visible_out_edges(self):
        return self._out_edges

    @property
    def visible_loops(self):
        return self._loops

    @property
    def hidden_in_edges(self):
        return self._hidden_in_edges

    @property
    def hidden_out_edges(self):
        return self._hidden_out_edges

    @property
    def hidden_loops(self):
        return self._hidden_loops

    @property
    def visible_edges(self):
        return self._in_edges | self._out_edges | self._loops

    @property
    def hidden_edges(self):
        return self._hidden_in_edges | self._hidden_out_edges | self._hidden_loops

    def add_in_edge(self, edge_id):
        self._in_edges.add(edge_id)

    def add_out_edge(self, edge_id):
        self._out_edges.add(edge_id)

    def add_loop(self, edge_id):
        self._loops.add(edge_id)

    def hide_in_edge(self, edge_id):
        self._in_edges.remove(edge_id)
        self._hidden_in_edges.add(edge_id)

    def hide_out_edge(self, edge_id):
        self._out_edges.remove(edge_id)
        self._hidden_out_edges.add(edge_id)

    def hide_loop(self, edge_id):
        self._loops.remove(edge_id)
        self._hidden_loops.add(edge_id)

    def restore_in_edge(self, edge_id):
        self._hidden_in_edges.remove(edge_id)
        self._in_edges.add(edge_id)

    def restore_out_edge(self, edge_id):
        self._hidden_out_edges.remove(edge_id)
        self._out_edges.add(edge_id)

    def restore_loop(self, edge_id):
        self._hidden_loops.remove(edge_id)
        self._loops.add(edge_id)

    def remove_in_edge(self, edge_id):
        self._in_edges.remove(edge_id)

    def remove_out_edge(self, edge_id):
        self._out_edges.remove(edge_id)

    def remove_loop(self, edge_id):
        self._loops.remove(edge_id)

