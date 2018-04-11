import matplotlib.pyplot as plt

from vertex import Vertex
from edge import Edge

class InteractiveGraph(object):

    def __init__(self, ax):

        self.ax = ax
        self.ax.set_aspect("equal")
        self.vertices = { }
        self.edges = { }

    def add_vertex(self, vx_id, xy, radius, label, **props):

        if vx_id in self.vertices:
            raise Exception("duplicate vertex id")

        c = plt.Circle(xy, radius, picker = True, **props)
        self.ax.add_patch(c)
        vx = Vertex(self, c, label)
        self.vertices[vx_id] = vx
        vx.connect()

    def add_edge(self, edge_id, src_id, tgt_id, **props):

        if src_id not in self.vertices or tgt_id not in self.vertices:
            raise Exception("nonexistent vertex")

        if edge_id in self.edges:
            raise Exeception("duplicate edge id")

        self.vertices[src_id].add_out_edge(edge_id)
        self.vertices[tgt_id].add_in_edge(edge_id)

        src, tgt = self.vertices[src_id], self.vertices[tgt_id]
        src_x, src_y = src.circle.center
        tgt_x, tgt_y = tgt.circle.center

        line = plt.Line2D([ src_x, tgt_x ], [ src_y, tgt_y ], **props)
        self.ax.add_line(line)
        edge = Edge(self, src_id, tgt_id, line)
        edge.update()
        self.edges[edge_id] = edge

    def reset_view(self):

        self.ax.set_autoscale_on(True)
        self.ax.relim()
        self.ax.autoscale_view()
        self.ax.figure.canvas.toolbar.update()

