import matplotlib.pyplot as plt

from vertex import Vertex
from edge import Edge

class InteractiveGraph(object):

    def __init__(self, ax):

        self.ax = ax
        self.ax.set_aspect("equal")
        self.vertices = { }
        self.edges = { }
        self.press_action = "drag"
        self.hidden_vertices = { }
        self.hidden_edges = { }

    def add_vertex(self, vx_id, xy, radius, label, **props):

        if vx_id in self.vertices:
            raise Exception("duplicate vertex id")

        c = plt.Circle(xy, radius, picker = True, **props)
        self.ax.add_patch(c)
        vx = Vertex(vx_id, self, c, label)
        self.vertices[vx_id] = vx
        vx.connect()

    def add_edge(self, edge_id, src_id, tgt_id, **props):

        if src_id not in self.vertices or tgt_id not in self.vertices:
            raise Exception("nonexistent vertex")

        if edge_id in self.edges:
            raise Exception("duplicate edge id")

        if src_id == tgt_id:
            self.vertices[src_id].add_loop(edge_id)
            self.edges[edge_id] = Edge(edge_id, self, src_id, tgt_id, None)
            return

        self.vertices[src_id].add_out_edge(edge_id)
        self.vertices[tgt_id].add_in_edge(edge_id)

        src, tgt = self.vertices[src_id], self.vertices[tgt_id]
        src_x, src_y = src.circle.center
        tgt_x, tgt_y = tgt.circle.center

        line = plt.Line2D([ src_x, tgt_x ], [ src_y, tgt_y ], **props)
        self.ax.add_line(line)
        edge = Edge(edge_id, self, src_id, tgt_id, line)
        edge.update()
        self.edges[edge_id] = edge

    def hide_vertex(self, vx_id):

        vertex = self.vertices[vx_id]

        for edge_id in vertex.in_edges:
            edge = self.edges.pop(edge_id)
            self.hidden_edges[edge_id] = edge
            self.vertices[edge.source].hide_out_edge(edge_id)
            edge.hide()

        for edge_id in vertex.out_edges:
            edge = self.edges.pop(edge_id)
            self.hidden_edges[edge_id] = edge
            self.vertices[edge.target].hide_in_edge(edge_id)
            edge.hide()

        for edge_id in vertex.loops:
            self.hidden_edges[edge_id] = self.edges.pop(edge_id)

        vertex.hide()
        self.hidden_vertices[vx_id] = self.vertices.pop(vx_id)
        self.ax.figure.canvas.draw()

    def restore_vertex(self, vx_id):

        if vx_id not in self.hidden_vertices:
            raise Exception("nonexistent vertex")

        vertex = self.hidden_vertices.pop(vx_id)
        self.vertices[vx_id] = vertex

        in_edges, out_edges = set(), set()
        for edge_id in vertex.hidden_in_edges:
            edge = self.hidden_edges[edge_id]
            if edge.source in self.vertices:
                self.edges[edge_id] = self.hidden_edges.pop(edge_id)
                in_edges.add(edge_id)
                self.vertices[edge.source].restore_out_edge(edge_id)
                edge.restore(self.ax)

        for edge_id in vertex.hidden_out_edges:
            edge = self.hidden_edges[edge_id]
            if edge.target in self.vertices:
                self.edges[edge_id] = self.hidden_edges.pop(edge_id)
                out_edges.add(edge_id)
                self.vertices[edge.target].restore_in_edge(edge_id)
                edge.restore(self.ax)

        for edge_id in vertex.hidden_loops:
            self.edges[edge_id] = self.hidden_edges.pop(edge_id)

        vertex.restore(self.ax, in_edges, out_edges)
        self.ax.figure.canvas.draw()

    def remove_vertex(self, vx_id):

        vertex = self.vertices.pop(vx_id)
        vertex.remove()

        for edge_id in vertex.loops:
            edge = self.edges.pop(edge_id)

        for edge_id in vertex.in_edges:
            edge = self.edges.pop(edge_id)
            src = self.vertices[edge.source]
            src.remove_out_edge(edge_id)

        for edge_id in vertex.out_edges:
            edge = self.edges.pop(edge_id)
            tgt = self.vertices[edge.target]
            tgt.remove_in_edge(edge_id)

        self.ax.figure.canvas.draw()

    def restore_all(self):

        for vx in self.hidden_vertices.keys():
            self.restore_vertex(vx)
            
    def reset_view(self):

        self.ax.set_autoscale_on(True)
        self.ax.relim()
        self.ax.autoscale_view()
        self.ax.figure.canvas.toolbar.update()

