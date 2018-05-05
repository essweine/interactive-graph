from exceptions import NonexistentVertexError

class ExpandableSubgraph(object):

    def __init__(self, graph):

        self._graph = graph
        self._collapsed, self._expanded = { }, { }

    def add(self, root, vertices, expanded_props = { }, collapsed_props = { }, state = "collapsed"):

        if not self._graph.vertex_exists(root):
            raise NonexistentVertexError(root, "create subgraph")

        edges = self._graph.get_edges(set([ root ]) | vertices)

        if state == "collapsed":
            # This is a little unintuitive, but collapse moves a vertex from expanded to collapsed
            self._expanded[root] = ExpandableSubgraphData(root, vertices, edges, expanded_props, collapsed_props)
            return self.collapse(root)

        elif state == "expanded":
            self._collapsed[root] = ExpandableSubgraphData(root, vertices, edges, expanded_props, collapsed_props)
            return self.expand(root)

    def remove(self, root):

        # Restore default artist
        if root in self.collapsed:
            self.expand(root)
        vertex = self._graph.get_vertex(root)
        vertex.update_circle()
        return self._expanded.pop(root)

    def expand_or_collapse(self, root):

        if root in self.collapsed:
            return self.expand(root)
        elif root in self.expanded:
            return self.collapse(root)
        else:
            pass

    def expand(self, root):

        vertex = self._graph.get_vertex(root)
        sg = self.get_subgraph(root)

        errors = [ ]
        errors.extend(self._graph.restore_vertices(sg.vertices - self._graph.visible_vertices))
        errors.extend(self._graph.restore_edges(sg.edges - self._graph.visible_edges))

        vertex.update_circle(**sg.expanded)
        self._expanded[root] = self._collapsed.pop(root)

        return errors

    def collapse(self, root):

        vertex = self._graph.get_vertex(root)
        sg = self.get_subgraph(root)

        for child in self.expanded & sg.vertices:
            self.collapse(child)

        errors = [ ]
        errors.extend(self._graph.hide_vertices(sg.vertices - self._graph.hidden_vertices))
        errors.extend(self._graph.hide_edges(sg.edges - self._graph.hidden_edges))

        vertex.update_circle(**sg.collapsed)
        self._collapsed[root] = self._expanded.pop(root)

        return errors

    def add_vertex(self, root, vx_id):

        if vx_id != root:
            sg = self.get_subgraph(root)
            sg.vertices.add(vx_id)
            sg.edges |= self._graph.filter_edges(vx_id, set([ root ]) | sg.vertices)

    def remove_vertex(self, root, vx_id):

        if vx_id == root:
            raise Exception("cannot remove root vertex from subgraph")
        sg = self.get_subgraph(root)
        sg.vertices.remove(vx_id)
        self.edges -= self._graph.filter_edges(vx_id, set([ root ]) | sg.vertices)

    def get_subgraph(self, root):

        if root in self.collapsed:
            return self._collapsed[root]
        elif root in self.expanded:
            return self._expanded[root]
        else:
            raise Exception("vertex is not the root of an exapndable subgraph")

    @property
    def collapsed(self):
        return set(self._collapsed.keys())

    @property
    def expanded(self):
        return set(self._expanded.keys())

class ExpandableSubgraphData(object):

    def __init__(self, root, vertices, edges, expanded_props, collapsed_props):

        self.root = root
        self.vertices = vertices
        self.edges = edges
        self.expanded = expanded_props
        self.collapsed = collapsed_props

