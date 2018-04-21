from exceptions import NonexistentVertexError

class ExpandableSubgraph(object):

    def __init__(self, graph, root, vertices = set(), state = "collapsed", 
            expanded_circle = None, collapsed_circle = None):

        if not graph.exists(root):
            raise NonexistentVertexError(root, "create expandable subgraph")

        self.state = state
        self.graph = graph
        self.root = root
        self.vertices = vertices
        self.edges = self._get_edges()

        circle = self.graph.get_vertex(root).circle
        if expanded_circle is None:
            self.expanded_circle = circle
        else:
            self.expanded_circle = expanded_circle

        if collapsed_circle is None:
            self.collapsed_circle = circle
        else:
            self.collapsed_circle = collapsed_circle

        self.collapse() if state == "collapsed" else self.expand()

    def expand_or_collapse(self):

        if self.state == "collapsed":
            self.expand()
        elif self.state == "expanded":
            self.collapse()

    def expand(self):

        # Handle errors or ignore them?
        root = self.graph.get_vertex(self.root)
        root.update_circle(self.expanded_circle, self.graph.ax)
        self.graph.restore_vertices(self.vertices - self.graph.visible_vertices)
        self.graph.restore_edges(self.edges - self.graph.visible_edges)
        self.state = "expanded"

    def collapse(self):

        root = self.graph.get_vertex(self.root)
        root.update_circle(self.collapsed_circle, self.graph.ax)
        self.graph.hide_vertices(self.vertices - self.graph.hidden_vertices)
        self.graph.hide_edges(self.edges - self.graph.hidden_edges)
        self.state = "collapsed"

    def remove(self, circle):

        root = self.graph.get_vertex(self.root)
        if circle is not None:
            root.update_circle(self.circle, self.graph.ax)

    def add_vertex(self, vx_id):

        if vx_id != self.root:
            self.vertices.add(vx_id)
        self.edges = self._get_edges()

    def remove_vertex(self, vx_id):

        if vx_id == self.root:
            raise Exception("cannot remove root vertex from subgraph")
        self.vertices.remove(vx_id)
        self.edges = self._get_edges()

    def _get_edges(self):

        edges = set()
        vertices = self.vertices | set([ self.root ])
        for vx_id in vertices:
            vertex = self.graph.get_vertex(vx_id)
            for edge_id in vertex.visible_edges | vertex.hidden_edges:
                edge = self.graph.get_edge(edge_id)
                if edge.source in vertices and edge.target in vertices:
                    edges.add(edge_id)
        return edges
