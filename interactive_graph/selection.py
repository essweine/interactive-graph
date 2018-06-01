from exceptions import NonexistentVertexError

class Selection(object):

    def __init__(self, graph, props = { }):

        self._graph = graph
        self._selected = set()
        self._selected_props = props
        self._complement = set()
        self._in_neighbors, self._out_neighbors = set(), set()

    def select_or_deselect(self, vxid):

        if vxid in self._selected:
            self._selected.remove(vxid)
            self._graph.restore_vertex_props(vxid)
            self._complement.add(vxid)
        else:
            self._selected.add(vxid)
            self._graph.update_vertex_props(vxid, **self._selected_props)
            if not self._complement:
                self._complement = self._graph.vertices - self._selected
            elif vxid in self._complement:
                self._complement.remove(vxid)
        self._update_neighbors()

    def hide_selection(self):

        self._graph.hide_vertices(self._selected & self._graph.visible_vertices)

    def restore_selection(self):

        self._graph.restore_vertices(self._selected & self._graph.hidden_vertices)

    def hide_complement(self):

        self._graph.hide_vertices(self._graph.visible_vertices - self._selected)

    def restore_complement(self):

        self._graph.restore_vertices(self._complement & self._graph.hidden_vertices)

    def hide_in_neighbors(self):

        self._graph.hide_vertices(self._in_neighbors & self._graph.visible_vertices)

    def restore_in_neighbors(self):

        self._graph.restore_vertices(self._in_neighbors & self._graph.hidden_vertices)

    def hide_out_neighbors(self):

        self._graph.hide_vertices(self._out_neighbors & self._graph.visible_vertices)

    def restore_out_neighbors(self):

        self._graph.restore_vertices(self._out_neighbors & self._graph.hidden_vertices)

    def remove_selection(self):

        self._graph.remove_vertices(self._selected)
        self._selected.clear()
        self._in_neighbors.clear()
        self._out_neighbors.clear()
        self._complement.clear()

    def deselect_all(self):

        self._graph.restore_vertices_props(self._selected)
        self._selected.clear()
        self._in_neighbors.clear()
        self._out_neighbors.clear()
        self._complement.clear()

    def add_vertices(self, vertices):

        self._selected |= vertices
        self._complement = self._graph.vertices - self._selected
        self._update_neighbors()
        if self.selected_props:
            self._graph.update_vertices_props(vertices, **self.selected_props)

    def remove_vertices(self, vertices):

        self._selected -= vertices
        self._complement = self._graph.vertices - self._selected
        self._update_neighbors()
        self._graph.restore_vertices_props(vertices)

    def _update_neighbors(self):

        self._in_neighbors.clear()
        self._out_neighbors.clear()
        for vxid in self._selected:
            vx = self._graph.get_vertex(vxid)
            for edge_id in vx.in_edges:
                self._in_neighbors.add(self._graph.get_edge(edge_id).source)
            for edge_id in vx.out_edges:
                self._out_neighbors.add(self._graph.get_edge(edge_id).target)
        self._in_neighbors -= self._selected
        self._out_neighbors -= self._selected

    def get_selection(self):

        return self._selected

    @property
    def selected_props(self):
        return self._selected_props


