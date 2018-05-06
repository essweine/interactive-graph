import matplotlib.pyplot as plt

from vertex import Vertex
from edge import Edge
from subgraph import ExpandableSubgraph
from exceptions import *

class InteractiveGraph(object):

    def __init__(self, ax):

        self.ax = ax
        self.ax.set_aspect("equal")

        self._visible_vertices, self._visible_edges = { }, { }
        self._hidden_vertices, self._hidden_edges = { }, { }

        self._press_action = "move"
        self._press_actions = {
            "move": None,
            "hide": self.hide_vertex,
            "remove": self.remove_vertex,
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

    def do_press_action(self, vx_id):

        self._press_actions[self._press_action](vx_id)

    def add_vertex(self, vx_id, xy, label, redraw = True, **props):

        if self.vertex_exists(vx_id):
            raise DuplicateVertexError(vx_id)

        vx = Vertex(vx_id, self, xy, label, **props)
        self._visible_vertices[vx_id] = vx

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

    def hide_vertex(self, vx_id, redraw = True):

        if not self.vertex_exists(vx_id):
            raise NonexistentVertexError(vx_id, "hide")
        elif not self.vertex_visible(vx_id):
            raise VertexActionError(vx_id, "hide", "vertex already hidden")

        vertex = self.get_vertex(vx_id)
        self._hidden_vertices[vx_id] = self._visible_vertices.pop(vx_id)

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

    def restore_vertex(self, vx_id, redraw = True):

        if not self.vertex_exists(vx_id):
            raise NonexistentVertexError(vx_id, "restore")
        if self.vertex_visible(vx_id):
            raise VertexActionError(vx_id, "restore", "vertex already visible")

        vertex = self.get_vertex(vx_id)

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

        self._visible_vertices[vx_id] = self._hidden_vertices.pop(vx_id)
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

    def remove_vertex(self, vx_id, redraw = True):

        if not self.vertex_exists(vx_id):
            raise NonexistentVertexError(vx_id, "remove")

        vertex = self._visible_vertices[vx_id]

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
            self._visible_vertices.pop(vx_id)
        else:
            self._hidden_vertices.pop(vx_id)

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
        return filter(lambda v: v is not None, [ self.add_vertex(*vx, **props) for vx in vertices ])

    @redraw
    def add_edges(self, edges, **props):
        return filter(lambda v: v is not None, [ self.add_edge(*e, **props) for e in edges ])

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

    def vertex_exists(self, vx_id):
        return vx_id in self.vertices

    def edge_exists(self, edge_id):
        return edge_id in self.edges

    def vertex_visible(self, vx_id):
        return vx_id in self.visible_vertices

    def edge_visible(self, edge_id):
        return edge_id in self.visible_edges

    def get_vertex(self, vx_id):

        if vx_id in self._visible_vertices:
            return self._visible_vertices[vx_id]
        elif vx_id in self._hidden_vertices:
            return self._hidden_vertices[vx_id]
        else:
            raise NonexistentVertexError(vx_id, "get")

    def get_edge(self, edge_id):

        if edge_id in self._visible_edges:
            return self._visible_edges[edge_id]
        elif edge_id in self._hidden_edges:
            return self._hidden_edges[edge_id]
        else:
            raise NonexistentVertexError(vx_id, "get")

    def get_edges(self, vertices):

        edges = set()
        for vx_id in vertices:
            vertex = self.get_vertex(vx_id)
            for edge_id in vertex.out_edges:
                edge = self.get_edge(edge_id)
                if edge.target in vertices:
                    edges.add(edge_id)
        return edges

    def filter_edges(self, vx_id, vertices):

        edges = set()
        vertex = self.get_vertex(vx_id)
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


