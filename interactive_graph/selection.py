class Selection(object):

    def __init__(self, graph, props = { }):

        self._graph = graph
        self._selected = set()
        self._selected_props = props

    def select_or_deselect(self, vx_id):

        vertex = self._graph.get_vertex(vx_id)
        if vx_id in self._selected:
            self._selected.remove(vx_id)
            vertex.update_circle()
        else:
            self._selected.add(vx_id)
            vertex.update_circle(**self._selected_props)

    def hide_selection(self, vx_id):

        if vx_id in self._selected:
            self._graph.hide_vertices(self._selected & self._graph.visible_vertices)

    def hide_complement(self, vx_id):

        if vx_id in self._selected:
            self._graph.hide_vertices(self._graph.visible_vertices - self._selected)

    def deselect_all(self):

        for vx_id in self._selected:
            vertex = self._graph.get_vertex(vx_id)
            vertex.update_circle()
        self._selected.clear()

    def get_selection(self):

        return self._selected
