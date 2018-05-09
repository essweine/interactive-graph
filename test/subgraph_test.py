import unittest
import numpy as np
import matplotlib.pyplot as plt

from interactive_graph.graph import InteractiveGraph
from interactive_graph.subgraph import ExpandableSubgraph

class TestExpandableSubgraph(unittest.TestCase):
    
    def setUp(self):

        fig, ax = plt.subplots()
        self.ig = InteractiveGraph(ax)
        self.sg = ExpandableSubgraph(self.ig)
        self.ig.add_press_action("expand/collapse", self.sg.expand_or_collapse)
        self.ig.set_press_action("expand/collapse")

        vprops, eprops = { "radius": 0.05, "color": (1.0, 0.0, 0.0) }, { "color": (0.0, 0.0, 0.0) }
        self.vertices, self.edges = [ ], [ ]

        for vid, xy in enumerate(np.random.rand(10, 2)):
            self.vertices.append((vid, xy, "vertex {n}".format(n = vid)))
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
        self.sg1_vertices = set(range(3))
        self.sg2_vertices = set(range(5, 8))
        self.sg3_vertices = set(range(8, 10))

        self.collapsed_props = { "radius": 0.1 }
        self.expanded_props = { "color": (0.0, 0.0, 0.0) }

    def test_expanded_subgraphs(self):

        sg1 = self.sg.add(self.sg1_root, self.sg1_vertices, self.expanded_props, self.collapsed_props, "expanded")
        sg2 = self.sg.add(self.sg2_root, self.sg2_vertices, self.expanded_props, self.collapsed_props, "expanded")

        self.assertItemsEqual(sg1, [ ], "create subgraph 1 returned with errors")
        self.assertItemsEqual(sg2, [ ], "create subgraph 2 returned with errors")
        self.assertItemsEqual(self.ig.visible_vertices, range(10), "vertices in expanded graphs are hidden")
        circle = self.ig.get_vertex(self.sg1_root)._circle
        self.assertEqual(circle.get_fc(), (0.0, 0.0, 0.0, 1.0), "expanded root circle does not appear in expanded graph")

        self.ig.do_press_action(self.sg1_root)
        circle = self.ig.get_vertex(self.sg1_root)._circle
        self.assertEqual(circle.get_radius(), 0.1, "collapsed root circle does not appear in collapsed graph")
        self.assertItemsEqual(self.ig.visible_vertices, range(3, 10), "vertices in collapsed graphs are visible")
        self.assertIn(24, self.ig.visible_edges, "edge from collapsed root to collapsed root is hidden")
        self.assertIn(25, self.ig.visible_edges, "edge from collapsed root to expanded root is hidden")
        self.assertNotIn(26, self.ig.visible_edges, "edge from collapsed graph to expanded graph is visible")

        self.ig.do_press_action(self.sg2_root)
        self.assertItemsEqual(self.ig.visible_vertices, set([ self.sg1_root, self.sg2_root ]) | self.sg3_vertices,
                "vertices in collapsed subgraphs are visible")
        self.assertIn(24, self.ig.visible_edges, "edge from collapsed root to collapsed root is hidden")
        self.assertNotIn(25, self.ig.visible_edges, "edge from collapsed graph to collapsed graph is visible")
        self.assertNotIn(26, self.ig.visible_edges, "edge from collapsed graph to expanded graph is visible")

    def test_collapsed_subgraphs(self):

        sg1 = self.sg.add(self.sg1_root, self.sg1_vertices, self.expanded_props, self.collapsed_props, "collapsed")
        sg2 = self.sg.add(self.sg2_root, self.sg2_vertices, self.expanded_props, self.collapsed_props, "collapsed")

        self.assertItemsEqual(sg1, [ ], "create subgraph 1 returned with errors")
        self.assertItemsEqual(sg2, [ ], "create subgraph 2 returned with errors")
        self.assertItemsEqual(self.ig.visible_vertices, [ self.sg1_root, self.sg2_root, 8, 9 ], 
                "vertices in collapsed subgraph are visible")
        circle = self.ig.get_vertex(self.sg1_root)._circle
        self.assertEqual(circle.get_radius(), 0.1, "collapsed root circle does not appear in collapsed graph")

        self.ig.do_press_action(self.sg1_root)
        circle = self.ig.get_vertex(self.sg1_root)._circle
        self.assertEqual(circle.get_fc(), (0.0, 0.0, 0.0, 1.0), "expanded root circle does not appear in expanded graph")
        self.assertItemsEqual(self.ig.visible_vertices, self.sg1_vertices | set([ self.sg1_root, self.sg2_root ]) | set([ 8, 9 ]), 
                "vertices in expanded graph are hidden")
        self.assertIn(24, self.ig.visible_edges, "edge from expanded root to collapsed root is hidden")
        self.assertNotIn(25, self.ig.visible_edges, "edge from expanded root to collapsed graph is visible")
        self.assertIn(26, self.ig.visible_edges, "edge from expanded graph to collapsed root is hidden")

        self.ig.do_press_action(self.sg2_root)
        self.assertItemsEqual(self.ig.visible_vertices, range(10), "vertices in expanded graphs are hidden")
        self.assertItemsEqual(self.ig.visible_edges, range(29), "edges in expanded graphs are hidden")

    def test_nested_subgraphs(self):

        sg1 = self.sg.add(self.sg1_root, self.sg1_vertices, self.expanded_props, self.collapsed_props, "collapsed")
        sg3 = self.sg.add(self.sg3_root, self.sg3_vertices, self.expanded_props, self.collapsed_props, "collapsed")
        sg2 = self.sg.add(self.sg2_root, self.sg2_vertices, self.expanded_props, self.collapsed_props, "collapsed")

        self.assertItemsEqual(sg1, [ ], "create subgraph 1 returned with errors")
        self.assertItemsEqual(sg2, [ ], "create subgraph 2 returned with errors")
        self.assertItemsEqual(sg3, [ ], "create subgraph 3 returned with errors")
        self.assertItemsEqual(self.ig.visible_vertices, [ self.sg1_root, self.sg2_root ], 
            "vertices in collapsed subgraph are visible")

        self.ig.do_press_action(self.sg2_root)
        self.assertItemsEqual(self.ig.visible_vertices, range(3, 8), "nested subgraph is visible")
        self.ig.do_press_action(self.sg3_root)
        self.assertItemsEqual(self.ig.visible_vertices, range(3, 10), "nested graph was not expanded")
        self.ig.do_press_action(self.sg2_root)
        self.ig.do_press_action(self.sg2_root)
        self.assertItemsEqual(self.ig.visible_vertices, range(3, 8), "nested graph was not collapsed")

if __name__ == '__main__':

    suite = unittest.TestLoader().loadTestsFromTestCase(TestExpandableSubgraph)
    unittest.TextTestRunner(verbosity=2).run(suite)
