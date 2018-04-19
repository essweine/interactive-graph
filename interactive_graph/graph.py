import matplotlib.pyplot as plt

from vertex import Vertex
from edge import Edge
from subgraph import ExpandableSubgraph
from exceptions import *

class InteractiveGraph(object):

    def __init__(self, ax):

        self.ax = ax
        self.ax.set_aspect("equal")
        self._vertices, self._edges = { }, { }
        self._hidden_vertices, self._hidden_edges = { }, { }
        self.press_action = "move"

    @property
    def visible_vertices(self):
        return set(self._vertices.keys())

    @property
    def visible_edges(self):
        return set(self._edges.keys())
    
    @property
    def hidden_vertices(self):
        return set(self._hidden_vertices.keys())
    
    @property
    def hidden_edges(self):
        return set(self._hidden_edges.keys())

    @property
    def expandable_subgraphs(self):
        return set(self._expandable_subgraphs.keys())

    def get_vertex(self, vx_id):

        if vx_id in self._vertices:
            return self._vertices[vx_id]
        elif vx_id in self._hidden_vertices:
            return self._hidden_vertices[vx_id]
        else:
            raise NonexistentVertexError(vx_id, "get")

    def get_edge(self, edge_id):

        if edge_id in self._edges:
            return self._edges[edge_id]
        elif edge_id in self._hidden_edges:
            return self._hidden_edges[edge_id]
        else:
            raise NonexistentVertexError(vx_id, "get")

    def get_expandable_subgraph(self, vx_id):

        if vx_id in self._expandable_subgraphs:
            return self._expandable_subgraphs[vx_id]

    def add_vertex(self, vx_id, xy, radius, label, redraw = True, **props):

        if vx_id in self._vertices:
            raise DuplicateVertexError(vx_id)

        c = plt.Circle(xy, radius, picker = True, **props)
        self.ax.add_patch(c)
        vx = Vertex(vx_id, self, c, label)
        self._vertices[vx_id] = vx
        vx.connect()

    def add_edge(self, edge_id, src_id, tgt_id, redraw = True, **props):

        if src_id not in self._vertices:
            raise NonexistentVertexError(src_id, "add edge")
        elif tgt_id not in self._vertices:
            raise NonexistentVertexError(tgt_id, "add edge")
            
        if edge_id in self._edges:
            edge = self._edges
            src, tgt = edge.source, edge.target
            raise DuplicateEdgeError(edge_id, src, tgt, "add edge", "edge id already exists")

        if src_id == tgt_id:
            self._vertices[src_id].add_loop(edge_id)
            self._edges[edge_id] = Edge(edge_id, self, src_id, tgt_id, None)
            return

        src, tgt = self._vertices[src_id], self._vertices[tgt_id]
        src_x, src_y = src.circle.center
        tgt_x, tgt_y = tgt.circle.center

        line = plt.Line2D([ src_x, tgt_x ], [ src_y, tgt_y ], **props)
        self.ax.add_line(line)
        edge = Edge(edge_id, self, src_id, tgt_id, line)
        edge.update()

        self._vertices[src_id].add_out_edge(edge_id)
        self._vertices[tgt_id].add_in_edge(edge_id)
        self._edges[edge_id] = edge

    def hide_vertex(self, vx_id, redraw = True):

        if vx_id in self._hidden_vertices:
            raise VertexActionError(vx_id, "hide", "vertex already hidden")
        elif vx_id not in self._vertices:
            raise NonexistentVertexError(vx_id, "hide")

        vertex = self._vertices[vx_id]

        for edge_id in vertex.loops:
            self._hidden_edges[edge_id] = self._edges.pop(edge_id)

        for edge_id in vertex.in_edges:
            edge = self._edges.pop(edge_id)
            self._hidden_edges[edge_id] = edge
            self._vertices[edge.source].hide_out_edge(edge_id)
            edge.hide()

        for edge_id in vertex.out_edges:
            edge = self._edges.pop(edge_id)
            self._hidden_edges[edge_id] = edge
            self._vertices[edge.target].hide_in_edge(edge_id)
            edge.hide()

        vertex.hide()
        self._hidden_vertices[vx_id] = self._vertices.pop(vx_id)
        if redraw:
            self.ax.figure.canvas.draw()

    def hide_edge(self, edge_id, redraw = True):

        if edge_id in self._hidden_edges:
            raise EdgeActionError(edge_id, "hide", "edge already hidden")
        elif edge_id not in self._edges:
            raise NonexistentEdgeError(edge_id, None, None, "hide")

        edge = self._edges[edge_id]
        src_id, tgt_id = edge.source, edge.target
        if src_id == tgt_id:
            self._vertices[src_id].hide_loop(edge_id)
        else:
            self._vertices[src_id].hide_out_edge(edge_id)
            self._vertices[tgt_id].hide_in_edge(edge_id)
            edge.hide()

        self._hidden_edges[edge_id] = self._edges.pop(edge_id)
        if redraw:
            self.ax.figure.canvas.draw()

    def restore_vertex(self, vx_id, redraw = True):

        if vx_id in self._vertices:
            raise VertexActionError(vx_id, "restore", "vertex already visible")
        elif vx_id not in self._hidden_vertices:
            raise NonexistentVertexError(vx_id, "restore")

        vertex = self._hidden_vertices[vx_id]
        self._vertices[vx_id] = vertex

        in_edges, out_edges = set(), set()
        for edge_id in vertex.hidden_in_edges:
            edge = self._hidden_edges[edge_id]
            if edge.source in self._vertices:
                self._edges[edge_id] = self._hidden_edges.pop(edge_id)
                in_edges.add(edge_id)
                self._vertices[edge.source].restore_out_edge(edge_id)
                edge.restore(self.ax)

        for edge_id in vertex.hidden_out_edges:
            edge = self._hidden_edges[edge_id]
            if edge.target in self._vertices:
                self._edges[edge_id] = self._hidden_edges.pop(edge_id)
                out_edges.add(edge_id)
                self._vertices[edge.target].restore_in_edge(edge_id)
                edge.restore(self.ax)

        for edge_id in vertex.hidden_loops:
            self._edges[edge_id] = self._hidden_edges.pop(edge_id)

        vertex.restore(self.ax, in_edges, out_edges)
        self._vertices[vx_id] = self._hidden_vertices.pop(vx_id)
        if redraw:
            self.ax.figure.canvas.draw()

    def restore_edge(self, edge_id, redraw = True):

        if edge_id in self._edges:
            edge = self._edges[edge_id]
            src_id, tgt_id = edge.source, edge.target
            raise EdgeActionError(edge_id, src_id, tgt_id,  "restore", "edge already visible")
        elif edge_id not in self._hidden_edges:
            raise NonexistentEdgeError(edge_id, None, None, "restore")

        edge = self._hidden_edges[edge_id]
        src_id, tgt_id = edge.source, edge.target

        if src_id in self._hidden_vertices:
            raise EdgeActionError(edge_id, src_id, tgt_id, "restore", "source vertex is hidden")
        if tgt_id in self._hidden_vertices:
            raise EdgeActionError(edge_id, src_id, tgt_id, "restore", "target vertex is hidden")

        if src_id == tgt_id:
            self._vertices[src_id].restore_loop(edge_id)
        else:
            self._vertices[src_id].restore_out_edge(edge_id)
            self._vertices[tgt_id].restore_in_edge(edge_id)
            edge.restore(self.ax)

        self._edges[edge_id] = self._hidden_edges.pop(edge_id)
        if redraw:
            self.ax.figure.canvas.draw()

    def remove_vertex(self, vx_id, redraw = True):

        if vx_id in self._hidden_vertices:
            self.restore_vertex(vx_id)
        if vx_id not in self._vertices:
            raise NonexistentVertexError(vx_id, "remove")

        vertex = self._vertices[vx_id]

        for edge_id in vertex.loops:
            edge = self._edges.pop(edge_id)

        for edge_id in vertex.in_edges:
            edge = self._edges.pop(edge_id)
            self._vertices[edge.source].remove_out_edge(edge_id)
            edge.hide()

        for edge_id in vertex.out_edges:
            edge = self._edges.pop(edge_id)
            self._vertices[edge.target].remove_in_edge(edge_id)
            edge.hide()

        vertex.remove()
        self._vertices.pop(vx_id)
        if redraw:
            self.ax.figure.canvas.draw()

    def remove_edge(self, edge_id, redraw = True):

        if edge_id in self._hidden_edges:
            self.restore_edge(edge_id)
        elif edge_id not in self._edges:
            raise NonexistentEdgeError(edge_id, "remove")

        edge = self._edges[edge_id]
        src_id, tgt_id = edge.source, edge.target
        if src_id == tgt_id:
            self._vertices[src_id].remove_loop(edge_id)
        else:
            self._vertices[src_id].remove_out_edge(edge_id)
            self._vertices[tgt_id].remove_in_edge(edge_id)
            edge.hide()

        self._edges.pop(edge_id)
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
            [ self.restore_vertex(vx, False) for vx in  self._hidden_vertices.keys() ] +
            [ self.restore_edge(e, False) for e in self._hidden_edges.keys() ])

    @redraw
    def clear(self):
        return filter(lambda v: v is not None, 
            [ self.remove_vertex(vx, False) for vx in self._hidden_vertices.keys() + self._vertices.keys() ] +
            [ self.remove_edge(e, False) for e in self._hidden_edges.keys() + self._edges.keys() ])

    def reset_view(self):

        self.ax.set_autoscale_on(True)
        self.ax.relim()
        self.ax.autoscale_view()
        self.ax.figure.canvas.toolbar.update()


