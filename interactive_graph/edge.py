import warnings
warnings.filterwarnings("error")

import matplotlib.pyplot as plt
import numpy as np
from numpy.linalg import norm

class Edge(object):

    def __init__(self, edge_id, graph, source, target, **props):

        self._edge_id = edge_id
        self._graph = graph
        self._source, self._target = source, target
        self._default_props = props

        if source != target:
            self._line = plt.Line2D([ 0, 0 ], [ 0, 0 ], **props)
            self._graph.ax.add_artist(self._line)
            self.update()
        else:
            self._line = None

    def hide(self):

        self._line.remove()

    def restore(self, ax):

        self.update()
        self._line.set_figure(ax.figure)
        ax.add_artist(self._line)

    def update(self):

        src, tgt = self._graph.get_vertex(self._source), self._graph.get_vertex(self._target)
        src_x, src_y = src._circle.center
        tgt_x, tgt_y = tgt._circle.center
        r1, r2 = src._circle.radius, tgt._circle.radius

        if src_y == tgt_y:
            if src_x < tgt_x:
                self._line.set_xdata([ src_x + r1, tgt_x - r2 ])
            else:
                self._line.set_xdata([ src_x - r1, tgt_x + r2 ])
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
            self._line.set_xdata([ src_x + dx * r1, tgt_x - dx * r2 ])
            self._line.set_ydata([ src_y + dy * r1, tgt_y - dy * r2 ])

        elif tgt_y < src_y:
            u1 = np.array([ src_x - 1, src_y ])
            try:
                a = np.arccos(np.dot((u1 - v1), (u2 - v1)))
                dx, dy = np.cos(a), np.sin(a)
            except RuntimeWarning:
                dx, dy = 0, 0
            self._line.set_xdata([ src_x - dx * r1, tgt_x + dx * r2 ])
            self._line.set_ydata([ src_y - dy * r1, tgt_y + dy * r2 ])

        #TODO: Arrows?

    @property
    def edge_id(self):
        return self._edge_id

    @property
    def default_props(self):
        return self._default_props

    @property
    def source(self):
        return self._source

    @property
    def target(self):
        return self._target
