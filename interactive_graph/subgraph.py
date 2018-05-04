from exceptions import NonexistentVertexError

class ExpandableSubgraph(object):

    def __init__(self, graph):

        self.graph = graph
        self._collapsed, self._expanded = { }, { }

    def add(self, root, vertices, expanded_circle = None, collapsed_circle = None, state = "collapsed"):

        if not self.graph.vertex_exists(root):
            raise NonexistentVertexError(root, "create subgraph")

        if expanded_circle is None:
            expanded_circle = self.graph.get_vertex(root).circle
        if collapsed_circle is None:
            collapsed_circle = self.graph.get_vertex(root).circle

        edges = self.graph.get_edges(set([ root ]) | vertices)

        if state == "collapsed":
            # This is a little unintuitive, but collapse moves a vertex from expanded to collapsed
            self._expanded[root] = ExpandableSubgraphData(root, vertices, edges, expanded_circle, collapsed_circle)
            return self.collapse(root)

        elif state == "expanded":
            self._collapsed[root] = ExpandableSubgraphData(root, vertices, edges, expanded_circle, collapsed_circle)
            return self.expand(root)

    def remove(self, root, circle = None):

        vertex = self.graph.get_vertex(root)
        sg = self.get_subgraph(root)
        sg.expand()
        if circle is not None:
            vertex.update_circle(circle, self.graph.ax)
        return self._expanded.pop(root)

    def expand_or_collapse(self, root):

        if root in self.collapsed:
            return self.expand(root)
        elif root in self.expanded:
            return self.collapse(root)
        else:
            pass

    def expand(self, root):

        vertex = self.graph.get_vertex(root)
        sg = self.get_subgraph(root)

        errors = [ ]
        errors.extend(self.graph.restore_vertices(sg.vertices - self.graph.visible_vertices))
        errors.extend(self.graph.restore_edges(sg.edges - self.graph.visible_edges))

        vertex.update_circle(sg.expanded_circle, self.graph.ax)
        self._expanded[root] = self._collapsed.pop(root)

        return errors

    def collapse(self, root):

        vertex = self.graph.get_vertex(root)
        sg = self.get_subgraph(root)

        for child in self.expanded & sg.vertices:
            self.collapse(child)

        errors = [ ]
        errors.extend(self.graph.hide_vertices(sg.vertices - self.graph.hidden_vertices))
        errors.extend(self.graph.hide_edges(sg.edges - self.graph.hidden_edges))

        vertex.update_circle(sg.collapsed_circle, self.graph.ax)
        self._collapsed[root] = self._expanded.pop(root)

        return errors

    def add_vertex(self, root, vx_id):

        if vx_id != root:
            sg = self.get_subgraph(root)
            sg.vertices.add(vx_id)
            sg.edges |= self.graph.filter_edges(vx_id, set([ root ]) | sg.vertices)

    def remove_vertex(self, root, vx_id):

        if vx_id == root:
            raise Exception("cannot remove root vertex from subgraph")
        sg = self.get_subgraph(root)
        sg.vertices.remove(vx_id)
        self.edges -= self.graph.filter_edges(vx_id, set([ root ]) | sg.vertices)

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

    def __init__(self, root, vertices, edges, expanded_circle, collapsed_circle):

        self.root = root
        self.vertices = vertices
        self.edges = edges
        self.expanded_circle = expanded_circle
        self.collapsed_circle = collapsed_circle

