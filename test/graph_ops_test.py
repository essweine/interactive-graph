import unittest
import numpy as np
import matplotlib.pyplot as plt

from interactive_graph.graph import InteractiveGraph

class TestGraphOps(unittest.TestCase):
    
    def setUp(self):
        
        fig, ax = plt.subplots()
        self.ig = InteractiveGraph(ax)
        for idx, xy in enumerate(np.random.rand(6, 2)):
            self.ig.add_vertex(idx, xy, 0.05, label = "vertex {n}".format(n = idx))
        edge_id = 0
        for v in range(1, 6):
            self.ig.add_edge(edge_id, 0, v)
            edge_id += 1
        self.ig.add_edge(edge_id, 1, 1)
        edge_id += 1
        for v in range(3, 5):
            self.ig.add_edge(edge_id, 2, v)
            edge_id += 1
        for v in range(3, 6):
            self.ig.add_edge(edge_id, 3, v)
            edge_id += 1
        self.ig.add_edge(edge_id, 4, 5)

    def test_hide_restore_in_order(self):

        self.ig.hide_vertex(0)
        self.assertEqual(len(self.ig.visible_edges), 7, 
          "number edges after hiding vertex 0 was %d, expected 7" % len(self.ig.visible_edges))
        self.assertEqual(len(self.ig.hidden_edges), 5, 
          "number of hidden edges after hiding vertex 0 was %d, expected 5" % len(self.ig.hidden_edges))
        self.ig.hide_vertex(1)
        self.assertEqual(len(self.ig.visible_edges), 6, 
          "number edges after hiding vertex 1 was %d, expected 6" % len(self.ig.visible_edges))
        self.assertEqual(len(self.ig.hidden_edges), 6, 
          "number of hidden edges after hiding vertex 1 was %d, expected 6" % len(self.ig.hidden_edges))
        self.ig.hide_vertex(2)
        self.assertEqual(len(self.ig.visible_edges), 4, 
          "number edges after hiding vertex 2 was %d, expected 8" % len(self.ig.visible_edges))
        self.assertEqual(len(self.ig.hidden_edges), 8, 
          "number of hidden edges after hiding vertex 2 was %d, expected 8" % len(self.ig.hidden_edges))
        self.ig.hide_vertex(3)
        self.assertEqual(len(self.ig.visible_edges), 1, 
          "number edges after hiding vertex 3 was %d, expected 1" % len(self.ig.visible_edges))
        self.assertEqual(len(self.ig.hidden_edges), 11, 
          "number of hidden edges after hiding vertex 3 was %d, expected 11" % len(self.ig.hidden_edges))
        self.ig.hide_vertex(4)
        self.assertEqual(len(self.ig.visible_edges), 0, 
          "number edges after hiding vertex 4 was %d, expected 0" % len(self.ig.visible_edges))
        self.assertEqual(len(self.ig.hidden_edges), 12, 
          "number of hidden edges after hiding vertex 4 was %d, expected 12" % len(self.ig.hidden_edges))

        self.ig.restore_vertex(0)
        self.assertEqual(len(self.ig.visible_edges), 1, 
          "number edges after restoring vertex 0 was %d, expected 1" % len(self.ig.visible_edges))
        self.assertEqual(len(self.ig.hidden_edges), 11, 
          "number of hidden edges after restoring vertex 0 was %d, expected 11" % len(self.ig.hidden_edges))
        self.ig.restore_vertex(1)
        self.assertEqual(len(self.ig.visible_edges), 3, 
          "number edges after restoring vertex 1 was %d, expected 3" % len(self.ig.visible_edges))
        self.assertEqual(len(self.ig.hidden_edges), 9, 
          "number of hidden edges after restoring vertex 1 was %d, expected 9" % len(self.ig.hidden_edges))
        self.ig.restore_vertex(2)
        self.assertEqual(len(self.ig.visible_edges), 4, 
          "number edges after restoring vertex 2 was %d, expected 8" % len(self.ig.visible_edges))
        self.assertEqual(len(self.ig.hidden_edges), 8, 
          "number of hidden edges after restoring vertex 2 was %d, expected 8" % len(self.ig.hidden_edges))
        self.ig.restore_vertex(3)
        self.assertEqual(len(self.ig.visible_edges), 8, 
          "number edges after restoring vertex 3 was %d, expected 8" % len(self.ig.visible_edges))
        self.assertEqual(len(self.ig.hidden_edges), 4, 
          "number of hidden edges after restoring vertex 3 was %d, expected 4" % len(self.ig.hidden_edges))
        self.ig.restore_vertex(4)
        self.assertEqual(len(self.ig.visible_edges), 12, 
          "number edges after restoring vertex 4 was %d, expected 12" % len(self.ig.visible_edges))
        self.assertEqual(len(self.ig.hidden_edges), 0, 
          "number of hidden edges after restoring vertex 4 was %d, expected xxi012" % len(self.ig.hidden_edges))

    def test_hide_reverse_order(self):

        self.ig.hide_vertex(5)
        self.assertEqual(len(self.ig.visible_edges), 9, 
          "number edges after hiding vertex 5 was %d, expected 9" % len(self.ig.visible_edges))
        self.assertEqual(len(self.ig.hidden_edges), 3, 
          "number of hidden edges after hiding vertex 5 was %d, expected 3" % len(self.ig.hidden_edges))
        self.ig.hide_vertex(4)
        self.assertEqual(len(self.ig.visible_edges), 6, 
          "number edges after hiding vertex 4 was %d, expected 6" % len(self.ig.visible_edges))
        self.assertEqual(len(self.ig.hidden_edges), 6, 
          "number of hidden edges after hiding vertex 4 was %d, expected 6" % len(self.ig.hidden_edges))
        self.ig.hide_vertex(3)
        self.assertEqual(len(self.ig.visible_edges), 3, 
          "number edges after hiding vertex 3 was %d, expected 3" % len(self.ig.visible_edges))
        self.assertEqual(len(self.ig.hidden_edges), 9, 
          "number of hidden edges after hiding vertex 3 was %d, expected 9" % len(self.ig.hidden_edges))
        self.ig.hide_vertex(2)
        self.assertEqual(len(self.ig.visible_edges), 2, 
          "number edges after hiding vertex 2 was %d, expected 2" % len(self.ig.visible_edges))
        self.assertEqual(len(self.ig.hidden_edges), 10, 
          "number of hidden edges after hiding vertex 2 was %d, expected 10" % len(self.ig.hidden_edges))
        self.ig.hide_vertex(1)
        self.assertEqual(len(self.ig.visible_edges), 0, 
          "number edges after hiding vertex 1 was %d, expected 0" % len(self.ig.visible_edges))
        self.assertEqual(len(self.ig.hidden_edges), 12, 
          "number of hidden edges after hiding vertex 1 was %d, expected 12" % len(self.ig.hidden_edges))

        self.ig.restore_vertex(5)
        self.assertEqual(len(self.ig.visible_edges), 1, 
          "number edges after restoring vertex 5 was %d, expected 1" % len(self.ig.visible_edges))
        self.assertEqual(len(self.ig.hidden_edges), 11, 
          "number of hidden edges after restoring vertex 5 was %d, expected 11" % len(self.ig.hidden_edges))
        self.ig.restore_vertex(4)
        self.assertEqual(len(self.ig.visible_edges), 3, 
          "number edges after restoring vertex 4 was %d, expected 3" % len(self.ig.visible_edges))
        self.assertEqual(len(self.ig.hidden_edges), 9, 
          "number of hidden edges after restoring vertex 4 was %d, expected 9" % len(self.ig.hidden_edges))
        self.ig.restore_vertex(3)
        self.assertEqual(len(self.ig.visible_edges), 7, 
          "number edges after restoring vertex 3 was %d, expected 7" % len(self.ig.visible_edges))
        self.assertEqual(len(self.ig.hidden_edges), 5, 
          "number of hidden edges after restoring vertex 3 was %d, expected 5" % len(self.ig.hidden_edges))
        self.ig.restore_vertex(2)
        self.assertEqual(len(self.ig.visible_edges), 10, 
          "number edges after restoring vertex 2 was %d, expected 10" % len(self.ig.visible_edges))
        self.assertEqual(len(self.ig.hidden_edges), 2, 
          "number of hidden edges after restoring vertex 2 was %d, expected 2" % len(self.ig.hidden_edges))
        self.ig.restore_vertex(1)
        self.assertEqual(len(self.ig.visible_edges), 12, 
          "number edges after restoring vertex 1 was %d, expected 12" % len(self.ig.visible_edges))
        self.assertEqual(len(self.ig.hidden_edges), 0, 
          "number of hidden edges after restoring vertex 1 was %d, expected 0" % len(self.ig.hidden_edges))

    def test_remove(self):

        self.ig.remove_vertex(0)
        self.assertEqual(len(self.ig.visible_edges), 7, 
          "number edges after removing vertex 0 was %d, expected 7" % len(self.ig.visible_edges))
        self.assertEqual(len(self.ig.hidden_edges), 0, 
          "number of hidden edges after removing vertex 0 was %d, expected 0" % len(self.ig.hidden_edges))
        self.ig.remove_vertex(1)
        self.assertEqual(len(self.ig.visible_edges), 6, 
          "number edges after removing vertex 1 was %d, expected 6" % len(self.ig.visible_edges))
        self.assertEqual(len(self.ig.hidden_edges), 0, 
          "number of hidden edges after removing vertex 1 was %d, expected 0" % len(self.ig.hidden_edges))
        self.ig.remove_vertex(2)
        self.assertEqual(len(self.ig.visible_edges), 4, 
          "number edges after removing vertex 2 was %d, expected 8" % len(self.ig.visible_edges))
        self.assertEqual(len(self.ig.hidden_edges), 0, 
          "number of hidden edges after removing vertex 2 was %d, expected 0" % len(self.ig.hidden_edges))
        self.ig.remove_vertex(3)
        self.assertEqual(len(self.ig.visible_edges), 1, 
          "number edges after removing vertex 3 was %d, expected 1" % len(self.ig.visible_edges))
        self.assertEqual(len(self.ig.hidden_edges), 0, 
          "number of hidden edges after removing vertex 3 was %d, expected 0" % len(self.ig.hidden_edges))
        self.ig.remove_vertex(4)
        self.assertEqual(len(self.ig.visible_edges), 0, 
          "number edges after removing vertex 4 was %d, expected 0" % len(self.ig.visible_edges))
        self.assertEqual(len(self.ig.hidden_edges), 0, 
          "number of hidden edges after removing vertex 4 was %d, expected 0" % len(self.ig.hidden_edges))
        self.ig.remove_vertex(5)
        self.assertEqual(len(self.ig.visible_vertices), 0,
          "number of vertices after removing all was %d, expected 0" % len(self.ig.visible_vertices))
        self.assertEqual(len(self.ig.hidden_vertices), 0,
          "number of hidden vertices after removing all was %d, expected 0" % len(self.ig.hidden_vertices))

    def test_hide_and_restore(self):

        self.ig.hide_edge(0)
        self.assertItemsEqual(self.ig.visible_edges, [ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11 ], "incorrect edge set after hiding edge 0")
        self.ig.hide_vertex(0)
        self.ig.hide_edge(5)
        self.assertItemsEqual(self.ig.visible_edges, [ 6, 7, 8, 9, 10, 11 ], "incorrect edge set after hiding edge 5")
        self.ig.hide_vertex(1)
        self.ig.hide_edge(6)
        self.assertItemsEqual(self.ig.visible_edges, [ 7, 8, 9, 10, 11 ], "incorrect edge set after hiding edge 6")
        self.ig.hide_vertex(2)
        self.ig.hide_edge(8)
        self.assertItemsEqual(self.ig.visible_edges, [ 9, 10, 11 ], "incorrect edge set after hiding edge 8")
        self.ig.hide_vertex(3)
        self.ig.hide_edge(11)
        self.assertItemsEqual(self.ig.visible_edges, [ ], "incorrect edge set after hiding edge 11")

        self.ig.restore_vertex(0)
        self.ig.restore_vertex(1)
        self.ig.restore_vertex(2)
        self.ig.restore_vertex(3)
        self.assertItemsEqual(self.ig.visible_edges, [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 ], "incorrect edge set after restoring all vertices")
        self.ig.restore_edge(11)
        self.assertItemsEqual(self.ig.visible_edges, [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11 ], "incorrect edge set after restoring edge 11")

if __name__ == '__main__':

    suite = unittest.TestLoader().loadTestsFromTestCase(TestGraphOps)
    unittest.TextTestRunner(verbosity = 2).run(suite)
