from exceptions import NonexistentVertexError

class Selection(object):

    def __init__(self, graph, props = { }):

        self._graph = graph
        self._selected = set()
        self._selected_props = props
        self._complement = set()      # Only needed for restoring state after hiding complement

    def select_or_deselect(self, vxid):

        if vxid in self._selected:
            self._selected.remove(vxid)
            self._graph.restore_vertex_props(vxid)
        else:
            self._selected.add(vxid)
            self._graph.update_vertex_props(vxid, **self._selected_props)

    def hide_selection(self):

        self._graph.hide_vertices(self._selected & self._graph.visible_vertices)

    def restore_selection(self):

        self._graph.restore_vertices(self._selected & self._graph.hidden_vertices)

    def hide_complement(self):

        self._complement = self._graph.visible_vertices - self._selected
        self._graph.hide_vertices(self._graph.visible_vertices - self._selected)

    def restore_complement(self):

        self._graph.restore_vertices(self._complement & self._graph.hidden_vertices)
        self._complement.clear()

    def deselect_all(self):

        self._graph.restore_vertices_props(self._selected)
        self._selected.clear()
        self._complement.clear()

    def add_vertices(self, vertices):

        self._selected |= vertices
        self._complement.clear()
        if self.selected_props:
            self._graph.update_vertices_props(vertices, **self.selected_props)

    def remove_vertices(self, vertices):

        self._selected -= vertices
        self._complement.clear()
        self._graph.restore_vertices_props(vertices)

    def get_selection(self):

        return self._selected

    @property
    def selected_props(self):
        return self._selected_props
