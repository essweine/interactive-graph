import matplotlib.pyplot as plt
from matplotlib.axes import Axes

from vertex import Vertex
from edge import Edge
from subgraph import ExpandableSubgraph
from exceptions import *

class InteractiveGraph(object):

    def __init__(self, ax):

        self.ax = Axes(ax.get_figure(), ax.get_position(original = True))
        self.ax.set_aspect("equal")
        self.ax.set_anchor("NE")

        self._visible_vertices, self._visible_edges = { }, { }
        self._hidden_vertices, self._hidden_edges = { }, { }

        self._press_action = "move"
        self._press_actions = {
            "move": None,
        }

    @property
    def press_actions(self):
        return self._press_actions.keys()

    def add_press_action(self, name, handler):
        self._press_actions[name] = handler

    def remove_press_action(self, name):
        del self._press_actions[name]

    def set_press_action(self, name):

        if name not in self._press_actions:
            raise Exception("Invalid action")
        self._press_action = name

    def do_press_action(self, vxid):

        self._press_actions[self._press_action](vxid)

    def add_vertex(self, vxid, xy, label, redraw = True, **props):

        if self.vertex_exists(vxid):
            raise DuplicateVertexError(vxid)

        circle = plt.Circle(xy, **props)
        self.ax.add_patch(circle)
        vx = Vertex(vxid, self, circle, label, props)
        vx._connect()
        self._visible_vertices[vxid] = vx

        if redraw:
            self.ax.figure.canvas.draw()

    def update_vertex_props(self, vxid, redraw = True, **props):

        vx = self.get_vertex(vxid)
        vx.update_circle_props(**props)
        if redraw:
            self.ax.figure.canvas.draw()

    def restore_vertex_props(self, vxid, redraw = True):

        vx = self.get_vertex(vxid)
        vx.restore_circle_props()
        if redraw:
            self.ax.figure.canvas.draw()

    def add_edge(self, edge_id, src_id, tgt_id, redraw = True, **props):

        if not self.vertex_exists(src_id):
            raise NonexistentVertexError(src_id, "add edge")
        elif not self.vertex_exists(tgt_id):
            raise NonexistentVertexError(tgt_id, "add edge")
            
        if self.edge_exists(edge_id):
            edge = self.get_edge(edge_id)
            src, tgt = edge.source, edge.target
            raise DuplicateEdgeError(edge_id, src, tgt, "add edge", "edge id already exists")

        if src_id == tgt_id:
            src = self.get_vertex(src_id)
            src.add_loop(edge_id)
        else:
            src, tgt = self.get_vertex(src_id), self.get_vertex(tgt_id)
            src.add_out_edge(edge_id)
            tgt.add_in_edge(edge_id)

        edge = Edge(edge_id, self, src_id, tgt_id, **props)

        if self.vertex_visible(src_id) and self.vertex_visible(tgt_id):
            self._visible_edges[edge_id] = edge
        else:
            self._hidden_edges[edge_id] = edge

    def hide_vertex(self, vxid, redraw = True):

        if not self.vertex_exists(vxid):
            raise NonexistentVertexError(vxid, "hide")
        elif not self.vertex_visible(vxid):
            raise VertexActionError(vxid, "hide", "vertex already hidden")

        vertex = self.get_vertex(vxid)
        self._hidden_vertices[vxid] = self._visible_vertices.pop(vxid)

        for edge_id in vertex.loops & self.visible_edges:
            self._hidden_edges[edge_id] = self._visible_edges.pop(edge_id)
        for edge_id in vertex.in_edges & self.visible_edges:
            self._hidden_edges[edge_id] = self._visible_edges.pop(edge_id)
            self.get_edge(edge_id).hide()
        for edge_id in vertex.out_edges & self.visible_edges:
            self._hidden_edges[edge_id] = self._visible_edges.pop(edge_id)
            self.get_edge(edge_id).hide()

        vertex.hide()

        if redraw:
            self.ax.figure.canvas.draw()

    def hide_edge(self, edge_id, redraw = True):

        if not self.edge_exists(edge_id):
            raise NonexistentEdgeError(edge_id, None, None, "hide")
        elif not self.edge_visible(edge_id):
            raise EdgeActionError(edge_id, "hide", "edge already hidden")

        self._hidden_edges[edge_id] = self._visible_edges.pop(edge_id)
        edge = self.get_edge(edge_id)
        if edge.source != edge.target:
            edge.hide()

        if redraw:
            self.ax.figure.canvas.draw()

    def restore_vertex(self, vxid, redraw = True):

        if not self.vertex_exists(vxid):
            raise NonexistentVertexError(vxid, "restore")
        if self.vertex_visible(vxid):
            raise VertexActionError(vxid, "restore", "vertex already visible")

        vertex = self.get_vertex(vxid)

        for edge_id in vertex.in_edges:
            edge = self.get_edge(edge_id)
            if self.vertex_visible(edge.source):
                self._visible_edges[edge_id] = self._hidden_edges.pop(edge_id)
                edge.restore(self.ax)

        for edge_id in vertex.out_edges:
            edge = self.get_edge(edge_id)
            if self.vertex_visible(edge.target):
                self._visible_edges[edge_id] = self._hidden_edges.pop(edge_id)
                edge.restore(self.ax)

        for edge_id in vertex.loops:
            self._visible_edges[edge_id] = self._hidden_edges.pop(edge_id)

        self._visible_vertices[vxid] = self._hidden_vertices.pop(vxid)
        vertex.restore(self.ax)

        if redraw:
            self.ax.figure.canvas.draw()

    def restore_edge(self, edge_id, redraw = True):

        if not self.edge_exists(edge_id):
            raise NonexistentEdgeError(edge_id, None, None, "restore")
        elif self.edge_visible(edge_id):
            edge = self.get_edge(edge_id)
            src_id, tgt_id = edge.source, edge.target
            raise EdgeActionError(edge_id, src_id, tgt_id,  "restore", "edge already visible")

        edge = self.get_edge(edge_id)
        src_id, tgt_id = edge.source, edge.target

        if not self.vertex_visible(src_id):
            raise EdgeActionError(edge_id, src_id, tgt_id, "restore", "source vertex is hidden")
        if not self.vertex_visible(tgt_id):
            raise EdgeActionError(edge_id, src_id, tgt_id, "restore", "target vertex is hidden")

        self._visible_edges[edge_id] = self._hidden_edges.pop(edge_id)
        if src_id != tgt_id:
            edge.restore(self.ax)

        if redraw:
            self.ax.figure.canvas.draw()

    def remove_vertex(self, vxid, redraw = True):

        if not self.vertex_exists(vxid):
            raise NonexistentVertexError(vxid, "remove")

        vertex = self._visible_vertices[vxid]

        for edge_id in vertex.loops & self.visible_edges:
            edge = self._visible_edges.pop(edge_id)
        for edge_id in vertex.loops & self.hidden_edges:
            edge = self._hidden_edges.pop(edge_id)

        for edge_id in (vertex.in_edges | vertex.out_edges) & self.visible_edges:
            edge = self._visible_edges.pop(edge_id)
            edge.hide()

        for edge_id in (vertex.in_edges | vertex.out_edges) & self.hidden_edges:
            edge = self._hidden_edges.pop(edge_id)
            edge.hide()

        if self.vertex_visible:
            self._visible_vertices.pop(vxid)
        else:
            self._hidden_vertices.pop(vxid)

        vertex.remove()

        if redraw:
            self.ax.figure.canvas.draw()

    def remove_edge(self, edge_id, redraw = True):

        if not self.edge_exists(edge_id):
            raise NonexistentEdgeError(edge_id, "remove")

        if self.edge_visible(edge_id):
            edge = self._visible_edges.pop(edge_id)
        else:
            edge = self._hidden_edges.pop(edge_id)

        src_id, tgt_id = edge.source, edge.target
        src, tgt = self.get_vertex(src_id), self.get_vertex(tgt_id)

        if src_id == tgt_id:
            src.remove_loop(edge_id)
        else:
            src.remove_out_edge(edge_id)
            tgt.remove_in_edge(edge_id)
            edge.hide()

        if redraw:
            self.ax.figure.canvas.draw()

    def redraw(action):

        def f(self, *args, **kwargs):
            result = action(self, *args, **kwargs)
            self.ax.figure.canvas.draw()
            return result
        return f

    @redraw
    def add_vertices(self, vertices, **props):
        return filter(lambda v: v is not None, [ self.add_vertex(*vx, redraw = False, **props) for vx in vertices ])

    @redraw
    def update_vertices_props(self, vertices, **props):
        return filter(lambda v: v is not None, [ self.update_vertex_props(vx, redraw = False, **props) for vx in vertices ])

    @redraw
    def restore_vertices_props(self, vertices):
        return filter(lambda v: v is not None, [ self.restore_vertex_props(vx, redraw = False) for vx in vertices ])

    @redraw
    def add_edges(self, edges, **props):
        return filter(lambda v: v is not None, [ self.add_edge(*e, redraw = False, **props) for e in edges ])

    @redraw
    def hide_vertices(self, vertices):
        return filter(lambda v: v is not None, [ self.hide_vertex(vx, False) for vx in vertices ])

    @redraw
    def hide_edges(self, edge_ids):
        return filter(lambda v: v is not None, [ self.hide_edge(e, False) for e in edge_ids ])

    @redraw
    def restore_vertices(self, vertices):
        return filter(lambda v: v is not None, [ self.restore_vertex(vx, False) for vx in vertices ])

    @redraw
    def restore_edges(self, edge_ids):
        return filter(lambda v: v is not None, [ self.restore_edge(e, False) for e in edge_ids ])

    @redraw
    def remove_vertices(self, vertices):
        return filter(lambda v: v is not None, [ self.remove_vertex(vx, False) for vx in vertices ])

    @redraw
    def remove_edges(self, edge_ids):
        return filter(lambda v: v is not None, [ self.remove_edge(e, False) for e in edge_ids ])

    @redraw
    def restore_all(self):
        return filter(lambda v: v is not None, 
            [ self.restore_vertex(vx, False) for vx in  self.hidden_vertices ] +
            [ self.restore_edge(e, False) for e in self.hidden_edges ])

    @redraw
    def clear(self):
        return filter(lambda v: v is not None, 
            [ self.remove_vertex(vx, False) for vx in self._hidden_vertices.keys() + self._visible_vertices.keys() ] +
            [ self.remove_edge(e, False) for e in self._hidden_edges.keys() + self._visible_edges.keys() ])

    @property
    def vertices(self):
        return set(self._visible_vertices.keys()) | set(self._hidden_vertices.keys())

    @property
    def edges(self):
        return set(self._visible_edges.keys()) | set(self._hidden_edges.keys())

    @property
    def visible_vertices(self):
        return set(self._visible_vertices.keys())

    @property
    def visible_edges(self):
        return set(self._visible_edges.keys())
    
    @property
    def hidden_vertices(self):
        return set(self._hidden_vertices.keys())
    
    @property
    def hidden_edges(self):
        return set(self._hidden_edges.keys())

    def vertex_exists(self, vxid):
        return vxid in self.vertices

    def edge_exists(self, edge_id):
        return edge_id in self.edges

    def vertex_visible(self, vxid):
        return vxid in self.visible_vertices

    def edge_visible(self, edge_id):
        return edge_id in self.visible_edges

    def get_vertex(self, vxid):

        if vxid in self._visible_vertices:
            return self._visible_vertices[vxid]
        elif vxid in self._hidden_vertices:
            return self._hidden_vertices[vxid]
        else:
            raise NonexistentVertexError(vxid, "get")

    def get_edge(self, edge_id):

        if edge_id in self._visible_edges:
            return self._visible_edges[edge_id]
        elif edge_id in self._hidden_edges:
            return self._hidden_edges[edge_id]
        else:
            raise NonexistentVertexError(vxid, "get")

    def get_edges(self, vertices):

        edges = set()
        for vxid in vertices:
            vertex = self.get_vertex(vxid)
            for edge_id in vertex.out_edges:
                edge = self.get_edge(edge_id)
                if edge.target in vertices:
                    edges.add(edge_id)
        return edges

    def filter_edges(self, vxid, vertices):

        edges = set()
        vertex = self.get_vertex(vxid)
        for edge_id in vertex.edges:
            edge = self.get_edges(edge_id)
            if edge.source in vertices or edge.target in vertices:
                edges.add(edge_id)
        return edges

    def reset_view(self):

        self.ax.set_autoscale_on(True)
        self.ax.relim()
        self.ax.autoscale_view()
        self.ax.figure.canvas.toolbar.update()


