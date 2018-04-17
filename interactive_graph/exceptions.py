class VertexError(Exception):

    def __init__(self, vertex, action, reason):
        self.vertex = vertex
        self.action = action
        self.message = "Action {a} could not be performed for vertex {v}: {r}".format(
          a = action, v = vertex, r = reason)

    def __str__(self):
        return self.message

class DuplicateVertexError(VertexError):
    def __init__(self, vertex):
        super(DuplicateVertexError, self).__init__(vertex, "add", "vertex already exists")

class NonexistentVertexError(VertexError):
    def __init__(self, vertex, action):
        super(NonexistentVertexError, self).__init__(vertex, action, "vertex does not exist")

class VertexActionError(VertexError):
    def __init__(self, vertex, action, message):
        super(DuplicateActionError, self).__init__(vertex, action, message)

class EdgeError(Exception):

    def __init__(self, edge, source, target, action, reason):

        self.edge = edge
        self.source = source
        self.target = target
        self.action = action
        self.message = "Action {a} could not be performed for edge {e} with source {s} and target {t}: {r}".format(
          a = action, e = edge, s = source, t = target, r = reason)

    def __str__(self):
        return self.message

class DuplicateEdgeError(EdgeError):
    def __init__(self, edge, source, target, action):
        super(DuplicateEdgeError, self).__init__(edge, source, target, action, "edge already exists")

class NonexistentEdgeActionError(EdgeError):
    def __init__(self, edge, source, target, action):
        super(DuplicateEdgeError, self).__init__(edge, source, target, action, "edge does not exist")

class EdgeActionError(EdgeError):
    def __init__(self, edge, source, target, action, reason):
        super(DuplicateEdgeError, self).__init__(edge, source, target, action, reason)

