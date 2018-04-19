import unittest
import numpy as np
import matplotlib.pyplot as plt

from interactive_graph.graph import InteractiveGraph

class TestBulkGraphOps(unittest.TestCase):
    
    def setUp(self):

        fig, ax = plt.subplots()
        self.ig = InteractiveGraph(ax)

        self.vprops, self.eprops = { "color": (1.0, 0.0, 0.0) }, { "color": (0.0, 0.0, 0.0) }
        self.vertices, self.edges = [ ], [ ]

        for vid, xy in enumerate(np.random.rand(6, 2)):
            self.vertices.append((vid, xy, 0.05, "vertex {n}".format(n = vid)))
        for eid, (v1, v2) in enumerate(zip(np.random.randint(0, 6, 15), np.random.randint(0, 6, 15))):
            self.edges.append((eid, v1, v2))

    def add_all(self):

        vx_results = self.ig.add_vertices(self.vertices, **self.vprops)
        edge_results = self.ig.add_edges(self.edges, **self.eprops)
        return vx_results, edge_results

    def hide_vertices(self):
        return self.ig.hide_vertices([ vid for vid, xy, r, l in self.vertices ])

    def hide_edges(self):
        return self.ig.hide_edges([ eid for eid, s, t in self.edges ])

    def test_bulk_add(self):

        vx_results, edge_results = self.add_all()
        self.assertItemsEqual(vx_results, [ ], "add vertices returned with errors")
        self.assertItemsEqual(edge_results, [ ], "add edge returned with errors")

    def test_bulk_hide_vertices(self):

        self.add_all()
        results = self.hide_vertices()
        self.assertItemsEqual(results, [ ], "hide vertices returned with errors")
        self.assertEqual(len(self.ig.visible_vertices), 0, 
          "number of vertices was %d, expected 0" % len(self.ig.visible_vertices))
        self.assertEqual(len(self.ig.hidden_vertices), 6,
          "number of hidden vertices was %d, expected 6" % len(self.ig.hidden_vertices))
        self.assertEqual(len(self.ig.visible_edges), 0, 
          "number of edges was %d, expected 0" % len(self.ig.visible_edges))
        self.assertEqual(len(self.ig.hidden_edges), 15,
          "number of hidden edges was %d, expected 15" % len(self.ig.hidden_edges))

    def test_bulk_hide_edges(self):

        self.add_all()
        results = self.hide_edges()
        self.assertItemsEqual(results, [ ], "hide edges returned with errors")
        self.assertEqual(len(self.ig.visible_vertices), 6, 
          "number of vertices was %d, expected 6" % len(self.ig.visible_vertices))
        self.assertEqual(len(self.ig.hidden_vertices), 0,
          "number of hidden vertices was %d, expected 0" % len(self.ig.hidden_vertices))
        self.assertEqual(len(self.ig.visible_edges), 0, 
          "number of edges was %d, expected 0" % len(self.ig.visible_edges))
        self.assertEqual(len(self.ig.hidden_edges), 15,
          "number of hidden edges was %d, expected 15" % len(self.ig.hidden_edges))

    def test_bulk_restore_vertices(self):

        self.add_all()
        self.hide_vertices()
        results = self.ig.restore_vertices([ vid for vid, xy, r, l in self.vertices ])
        self.assertItemsEqual(results, [ ], "restore vertices returned with errors")
        self.assertEqual(len(self.ig.visible_vertices), 6, 
          "number of vertices was %d, expected 6" % len(self.ig.visible_vertices))
        self.assertEqual(len(self.ig.hidden_vertices), 0,
          "number of hidden vertices was %d, expected 0" % len(self.ig.hidden_vertices))
        self.assertEqual(len(self.ig.visible_edges), 15, 
          "number of edges was %d, expected 15" % len(self.ig.visible_edges))
        self.assertEqual(len(self.ig.hidden_edges), 0,
          "number of hidden edges was %d, expected 0" % len(self.ig.hidden_edges))

    def test_bulk_restore_edges(self):

        self.add_all()
        self.hide_edges()
        results = self.ig.restore_edges([ eid for eid, s, t in self.edges ])
        self.assertItemsEqual(results, [ ], "restore edges returned with errors")
        self.assertEqual(len(self.ig.visible_vertices), 6, 
          "number of vertices was %d, expected 6" % len(self.ig.visible_vertices))
        self.assertEqual(len(self.ig.hidden_vertices), 0,
          "number of hidden vertices was %d, expected 0" % len(self.ig.hidden_vertices))
        self.assertEqual(len(self.ig.visible_edges), 15, 
          "number of edges was %d, expected 15" % len(self.ig.visible_edges))
        self.assertEqual(len(self.ig.hidden_edges), 0,
          "number of hidden edges was %d, expected 0" % len(self.ig.hidden_edges))

    def test_bulk_remove_vertices(self):

        self.add_all()
        results = self.ig.remove_vertices([ vid for vid, xy, r, l in self.vertices ])
        self.assertItemsEqual(results, [ ], "remove vertices returned with errors")
        self.assertEqual(len(self.ig.visible_vertices), 0, 
          "number of vertices was %d, expected 0" % len(self.ig.visible_vertices))
        self.assertEqual(len(self.ig.hidden_vertices), 0,
          "number of hidden vertices was %d, expected 0" % len(self.ig.hidden_vertices))
        self.assertEqual(len(self.ig.visible_edges), 0, 
          "number of edges was %d, expected 0" % len(self.ig.visible_edges))
        self.assertEqual(len(self.ig.hidden_edges), 0,
          "number of hidden edges was %d, expected 0" % len(self.ig.hidden_edges))

    def test_bulk_remove_edges(self):

        self.add_all()
        results = self.ig.remove_edges([ eid for eid, s, t in self.edges ])
        self.assertItemsEqual(results, [ ], "remove edges returned with errors")
        self.assertEqual(len(self.ig.visible_vertices), 6, 
          "number of vertices was %d, expected 6" % len(self.ig.visible_vertices))
        self.assertEqual(len(self.ig.hidden_vertices), 0,
          "number of hidden vertices was %d, expected 0" % len(self.ig.hidden_vertices))
        self.assertEqual(len(self.ig.visible_edges), 0, 
          "number of edges was %d, expected 0" % len(self.ig.visible_edges))
        self.assertEqual(len(self.ig.hidden_edges), 0,
          "number of hidden edges was %d, expected 0" % len(self.ig.hidden_edges))

if __name__ == '__main__':

    suite = unittest.TestLoader().loadTestsFromTestCase(TestBulkGraphOps)
    unittest.TextTestRunner(verbosity=2).run(suite)
