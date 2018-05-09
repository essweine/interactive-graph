import matplotlib.pyplot as plt
import matplotlib.artist as mplartist
from copy import deepcopy

class Vertex(object):

    _lock = None
    annotation_props = dict(boxstyle = "square", fc = (0.2, 0.2, 0.2, 0.6), ec = (0.2, 0.2, 0.2, 0.8))

    def __init__(self, vertex_id, graph, circle, label = "", props = { }):

        self._vertex_id = vertex_id
        if props:
            self._default_props = props
        else:
            self._default_props = circle.properties()
        self._graph = graph
        self._circle = circle

        x, y = self._circle.center
        self._annotation = self._circle.axes.text(x, y, label, bbox = Vertex.annotation_props, visible = False)

        self._vertices = set()
        self._in_edges = set()
        self._out_edges = set()
        self._loops = set()

        self._press = None
        self._background = None

    def hide(self):

        if self._annotation.get_visible() is True:
            self._annotation.set_visible(False)
        self._circle.remove()

    def restore(self, ax):

        self._circle.set_figure(ax.figure)
        ax.add_artist(self._circle)

    def remove(self):

        self._annotation.remove()
        self._circle.remove()

    def update_circle_props(self, **props):

        mplartist.setp(self._circle, **props)
        for edge in (self.in_edges | self.out_edges) & self._graph.visible_edges:
            artist = self._graph.get_edge(edge)
            artist.update()

    def restore_circle_props(self):

        mplartist.setp(self._circle, **self.default_props)
        for edge in (self.in_edges | self.out_edges) & self._graph.visible_edges:
            artist = self._graph.get_edge(edge)
            artist.update()

    def _on_press(self, event):

        if event.inaxes != self._circle.axes:
            return

        contains, attrd = self._circle.contains(event)
        if not contains:
            return

        if self._graph._press_action == "move":
            self._move(event)
        else:
            self._graph.do_press_action(self._vertex_id)

    def _move(self, event):

        if Vertex._lock is not None:
            return

        Vertex._lock = self

        if self._annotation.get_visible() is True:
            self._annotation.set_visible(False)

        x0, y0 = event.xdata, event.ydata
        self._press = x0, y0, event.xdata, event.ydata

        canvas = self._circle.figure.canvas
        axes = self._circle.axes
        self._circle.set_animated(True)
        canvas.draw()
        self._background = canvas.copy_from_bbox(self._circle.axes.bbox)
        axes.draw_artist(self._circle)
        canvas.blit(axes.bbox)

    def _on_motion(self, event):

        if event.inaxes != self._circle.axes:
            return

        contains, attrd = self._circle.contains(event)
        if not contains and self._annotation.get_visible() is True:
            self._annotation.set_visible(False)
            self._annotation.figure.canvas.draw()
        if contains and self._press is None:
            self._annotation.set_visible(True)
            self._annotation.figure.canvas.draw()

        if self._press is None:
            return

        if Vertex._lock is not self:
            return

        x0, y0, xpress, ypress = self._press
        dx, dy = event.xdata - xpress, event.ydata - ypress
        self._circle.center = (x0 + dx, y0 + dy)

        for edge in (self.in_edges | self.out_edges) & self._graph.visible_edges:
            artist = self._graph.get_edge(edge)
            artist.update()

        canvas = self._circle.figure.canvas
        axes = self._circle.axes
        canvas.restore_region(self._background)
        axes.draw_artist(self._circle)
        canvas.blit(axes.bbox)

    def _on_release(self, event):

        if Vertex._lock is not self:
            return

        for edge in (self.in_edges | self.out_edges) & self._graph.visible_edges:
            artist = self._graph.get_edge(edge)
            artist.update()

        self._press = None
        Vertex._lock = None
        self._circle.set_animated(False)
        self._background = None
        self._circle.figure.canvas.draw()

        x, y = self._circle.center
        self._annotation.set_x(x), self._annotation.set_y(y)

    def _connect(self):

        self._cidpress = self._circle.figure.canvas.mpl_connect("button_press_event", self._on_press)
        self._cidrelease = self._circle.figure.canvas.mpl_connect("button_release_event", self._on_release)
        self._cidmotion = self._circle.figure.canvas.mpl_connect("motion_notify_event", self._on_motion)

    def _disconnect(self):

        self._circle.figure.canvas.mpl_disconnect(self._cidpress)
        self._circle.figure.canvas.mpl_disconnect(self._cidrelease)
        self._circle.figure.canvas.mpl_disconnect(self._cidmotion)

    @property
    def vertex_id(self):
        return self._vertex_id

    @property
    def default_props(self):
        return self._default_props

    @property
    def in_edges(self):
        return self._in_edges

    @property
    def out_edges(self):
        return self._out_edges

    @property
    def loops(self):
        return self._loops

    def add_in_edge(self, edge_id):
        self._in_edges.add(edge_id)

    def add_out_edge(self, edge_id):
        self._out_edges.add(edge_id)

    def add_loop(self, edge_id):
        self._loops.add(edge_id)

    def remove_in_edge(self, edge_id):
        self._in_edges.remove(edge_id)

    def remove_out_edge(self, edge_id):
        self._out_edges.remove(edge_id)

    def remove_loop(self, edge_id):
        self._loops.remove(edge_id)

