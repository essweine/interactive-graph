class Selection(object):

    def __init__(self, graph, props = { }):

        self._graph = graph
        self._selected = set()
        self._selected_props = props

    def select_or_deselect(self, vxid):

        if vxid in self._selected:
            self._selected.remove(vxid)
            self._graph.restore_vertex_props(vxid)
        else:
            self._selected.add(vxid)
            self._graph.update_vertex_props(**self._selected_props)

    def hide_selection(self, vxid):

        if vxid in self._selected:
            self._graph.hide_vertices(self._selected & self._graph.visible_vertices)

    def hide_complement(self, vxid):

        if vxid in self._selected:
            self._graph.hide_vertices(self._graph.visible_vertices - self._selected)

    def deselect_all(self):

        self._graph.restore_vertices_props(self._selected)
        self._selected.clear()

    def get_selection(self):

        return self._selected
