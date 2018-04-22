import unittest
import numpy as np
import matplotlib.pyplot as plt

from interactive_graph.graph import InteractiveGraph
from interactive_graph.subgraph import ExpandableSubgraph

class TestExpandableSubgraph(unittest.TestCase):
    
    def setUp(self):

        fig, ax = plt.subplots()
        self.ig = InteractiveGraph(ax)

        vprops, eprops = { "color": (1.0, 0.0, 0.0) }, { "color": (0.0, 0.0, 0.0) }
        self.vertices, self.edges = [ ], [ ]

        for vid, xy in enumerate(np.random.rand(10, 2)):
            self.vertices.append((vid, xy, 0.05, "vertex {n}".format(n = vid)))
        for eid, (v1, v2) in enumerate(zip(np.random.randint(0, 4, 12), np.random.randint(0, 4, 12))):
            self.edges.append((eid, v1, v2))
        for eid, (v1, v2) in enumerate(zip(np.random.randint(4, 8, 12), np.random.randint(4, 8, 12))):
            self.edges.append((eid + 12, v1, v2))
        self.edges.append((24, 3, 4))
        self.edges.append((25, 3, 5))
        self.edges.append((26, 4, 2))
        self.edges.append((27, 7, 8))
        self.edges.append((28, 7, 9))

        self.ig.add_vertices(self.vertices, **vprops)
        self.ig.add_edges(self.edges, **eprops)

        self.sg1_root, self.sg2_root, self.sg3_root = 3, 4, 7
        self.sg1_vertices = range(3)
        self.sg2_vertices = range(5, 8)
        self.sg3_vertices = range(8, 10)

        c1, c2 = self.ig.get_vertex(3).circle, self.ig.get_vertex(4).circle
        self.sg1_collapsed_circle = plt.Circle(c1.center, 0.05, **vprops)
        self.sg2_collapsed_circle = plt.Circle(c2.center, 0.05, **vprops)
        self.sg1_expanded_circle = plt.Circle(c1.center, 0.05, **vprops)
        self.sg2_expanded_circle = plt.Circle(c2.center, 0.05, **vprops)

    def create_subgraph(self, root, vertices, state, cc, ec):

        return self.ig.create_expandable_subgraph(root, vertices, state = state, collapsed_circle = cc, expanded_circle = ec)

    def test_expanded_subgraphs(self):

        sg1 = self.create_subgraph(self.sg1_root, self.sg1_vertices, 
                state = "expanded", cc = self.sg1_collapsed_circle, ec = self.sg1_expanded_circle)
        sg2 = self.create_subgraph(self.sg2_root, self.sg2_vertices, 
                state = "expanded", cc = self.sg2_collapsed_circle, ec = self.sg2_expanded_circle)
        self.assertItemsEqual(sg1, [ ], "create subgraph 1 returned with errors")
        self.assertItemsEqual(sg2, [ ], "create subgraph 2 returned with errors")
        self.assertItemsEqual(self.ig.visible_vertices, range(10), "vertices in expanded graphs are hidden")
        sg2_circle = self.ig.get_vertex(4).circle
        self.assertEqual(sg2_circle, self.sg2_expanded_circle, "expanded root circle does not appear in expanded graph")

        self.ig.expand_or_collapse(3)
        sg1_circle = self.ig.get_vertex(3).circle
        self.assertEqual(sg1_circle, self.sg1_collapsed_circle, "collapsed root circle does not appear in collapsed graph")
        self.assertItemsEqual(self.ig.visible_vertices, range(3, 10), "vertices in collapsed graphs are visible")
        self.assertIn(24, self.ig.visible_edges, "edge from collapsed root to collapsed root is hidden")
        self.assertIn(25, self.ig.visible_edges, "edge from collapsed root to expanded root is hidden")
        self.assertNotIn(26, self.ig.visible_edges, "edge from collapsed graph to expanded graph is visible")

        self.ig.expand_or_collapse(4)
        self.assertItemsEqual(self.ig.visible_vertices, [ self.sg1_root, self.sg2_root ] + self.sg3_vertices,
                "vertices in collapsed subgraphs are visible")
        self.assertIn(24, self.ig.visible_edges, "edge from collapsed root to collapsed root is hidden")
        self.assertNotIn(25, self.ig.visible_edges, "edge from collapsed graph to collapsed graph is visible")
        self.assertNotIn(26, self.ig.visible_edges, "edge from collapsed graph to expanded graph is visible")

    def test_collapsed_subgraphs(self):

        sg1 = self.create_subgraph(self.sg1_root, self.sg1_vertices, 
                state = "collapsed", cc = self.sg1_collapsed_circle, ec = self.sg1_expanded_circle)
        sg2 = self.create_subgraph(self.sg2_root, self.sg2_vertices, 
                state = "collapsed", cc = self.sg2_collapsed_circle, ec = self.sg2_expanded_circle)
        self.assertItemsEqual(sg1, [ ], "create subgraph 1 returned with errors")
        self.assertItemsEqual(sg2, [ ], "create subgraph 2 returned with errors")
        self.assertItemsEqual(self.ig.visible_vertices, [ self.sg1_root, self.sg2_root, 8, 9 ],
          "vertices in collapsed subgraph are visible")
        sg2_circle = self.ig.get_vertex(4).circle
        self.assertEqual(sg2_circle, self.sg2_collapsed_circle, "collapsed root circle does not appear in collapsed graph")

        self.ig.expand_or_collapse(3)
        sg1_circle = self.ig.get_vertex(3).circle
        self.assertEqual(sg1_circle, self.sg1_expanded_circle, "expanded root circle does not appear in expanded graph")
        self.assertItemsEqual(self.ig.visible_vertices, self.sg1_vertices + [ self.sg1_root, self.sg2_root ] + [ 8, 9 ],
          "vertices in expanded graph are visible")
        self.assertIn(24, self.ig.visible_edges, "edge from expanded root to collapsed root is hidden")
        self.assertNotIn(25, self.ig.visible_edges, "edge from expanded root to collapsed graph is visible")
        self.assertIn(26, self.ig.visible_edges, "edge from expanded graph to collapsed root is hidden")

        self.ig.expand_or_collapse(4)
        self.assertItemsEqual(self.ig.visible_vertices, range(10), "vertices in expanded graphs are hidden")
        self.assertItemsEqual(self.ig.visible_edges, range(29), "edges in expanded graphs are hidden")

    def test_nested_subgraphs(self):

        sg1 = self.create_subgraph(self.sg1_root, self.sg1_vertices, 
                state = "collapsed", cc = self.sg1_collapsed_circle, ec = self.sg1_expanded_circle)
        sg3 = self.create_subgraph(self.sg3_root, self.sg3_vertices, state = "collapsed", cc = None, ec = None)
        sg2 = self.create_subgraph(self.sg2_root, self.sg2_vertices, 
                state = "collapsed", cc = self.sg2_collapsed_circle, ec = self.sg2_expanded_circle)
        self.assertItemsEqual(sg1, [ ], "create subgraph 1 returned with errors")
        self.assertItemsEqual(sg2, [ ], "create subgraph 2 returned with errors")
        self.assertItemsEqual(sg3, [ ], "create subgraph 3 returned with errors")
        self.assertItemsEqual(self.ig.visible_vertices, [ self.sg1_root, self.sg2_root ],
          "vertices in collapsed subgraph are visible")

        self.ig.expand_or_collapse(4)
        self.assertItemsEqual(self.ig.visible_vertices, range(3, 8), "nested subgraph is visible")
        self.ig.expand_or_collapse(7)
        self.assertItemsEqual(self.ig.visible_vertices, range(3, 10), "nested graph was not expanded")
        self.ig.expand_or_collapse(4)
        self.ig.expand_or_collapse(4)
        self.assertItemsEqual(self.ig.visible_vertices, range(3, 8), "nested graph was not collapsed")

if __name__ == '__main__':

    suite = unittest.TestLoader().loadTestsFromTestCase(TestExpandableSubgraph)
    unittest.TextTestRunner(verbosity=2).run(suite)
