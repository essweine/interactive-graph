import matplotlib.pyplot as plt
import numpy as np
from numpy.linalg import norm

class Edge(object):

    def __init__(self, edge_id, graph, source, target, **props):

        self.edge_id = edge_id
        self.graph = graph
        self.source, self.target = source, target
        self.default_props = props

        if source != target:
            self.line = plt.Line2D([ 0, 0 ], [ 0, 0 ], **props)
            self.graph.ax.add_artist(self.line)
            self.update()
        else:
            self.line = None

    def hide(self):

        self.line.remove()

    def restore(self, ax):

        self.update()
        self.line.set_figure(ax.figure)
        ax.add_artist(self.line)

    def update(self):

        src, tgt = self.graph.get_vertex(self.source), self.graph.get_vertex(self.target)
        src_x, src_y = src.circle.center
        tgt_x, tgt_y = tgt.circle.center
        r1, r2 = src.circle.radius, tgt.circle.radius

        if src_y == tgt_y:
            if src_x < tgt_x:
                self.line.set_xdata([ src_x + r1, tgt_x - r2 ])
            else:
                self.line.set_xdata([ src_x - r1, tgt_x + r2 ])
            return

        v1, v2 = np.array([ src_x, src_y ]), np.array([ tgt_x, tgt_y ])
        h = norm(v2 - v1)
        u2 = v1 + (v2 - v1) / h

        if src_y < tgt_y:
            u1 = np.array([ src_x + 1, src_y ])
            try:
                a = np.arccos(np.dot((u1 - v1), (u2 - v1)))
                dx, dy = np.cos(a), np.sin(a)
            except RuntimeWarning:
                dx, dy = 0, 0
            self.line.set_xdata([ src_x + dx * r1, tgt_x - dx * r2 ])
            self.line.set_ydata([ src_y + dy * r1, tgt_y - dy * r2 ])

        elif tgt_y < src_y:
            u1 = np.array([ src_x - 1, src_y ])
            try:
                a = np.arccos(np.dot((u1 - v1), (u2 - v1)))
                dx, dy = np.cos(a), np.sin(a)
            except RuntimeWarning:
                dx, dy = 0, 0
            self.line.set_xdata([ src_x - dx * r1, tgt_x + dx * r2 ])
            self.line.set_ydata([ src_y - dy * r1, tgt_y + dy * r2 ])

        #TODO: Arrows?

