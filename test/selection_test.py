import unittest
import numpy as np
import matplotlib.pyplot as plt

from interactive_graph.graph import InteractiveGraph
from interactive_graph.selection import Selection

class TestSelection(unittest.TestCase):

    def setUp(self):
        
        fig, ax = plt.subplots()
        self.ig = InteractiveGraph(ax)

        self.vprops, eprops = { "radius": 0.05, "color": (1.0, 0.0, 0.0) }, { "color": (0.0, 0.0, 0.0) }
        self.selected_props = { "radius": 0.1 }

        self.selection = Selection(self.ig, self.selected_props)
        self.ig.add_press_action("select/deselect", self.selection.select_or_deselect)
        self.ig.set_press_action("select/deselect")

        for idx, xy in enumerate(np.random.rand(6, 2)):
            self.ig.add_vertex(idx, xy, label = "vertex {n}".format(n = idx), **self.vprops)
        edge_id = 0
        for v in range(1, 6):
            self.ig.add_edge(edge_id, 0, v, **eprops)
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

    def test_select_deselect(self):

        self.ig.do_press_action(0)
        self.ig.do_press_action(1)
        self.ig.do_press_action(2)
        self.assertItemsEqual(self.selection.get_selection(), [ 0, 1, 2 ], "current selection is incorrect")
        circle = self.ig.get_vertex(0)._circle
        self.assertEqual(circle.get_radius(), self.selected_props["radius"], "selected vertex radius was not updated")
        self.ig.do_press_action(0)
        self.assertEqual(circle.get_radius(), self.vprops["radius"], "deselected vertex radius was not updated")
        self.assertItemsEqual(self.selection.get_selection(), [ 1, 2 ], "current selection is incorrect")

    def test_hide_and_restore_selection(self):

        self.ig.do_press_action(0)
        self.ig.do_press_action(1)
        self.ig.do_press_action(2)
        self.selection.hide_selection()
        self.assertItemsEqual(self.ig.hidden_vertices, [ 0, 1, 2 ], "selection is not hidden")
        self.selection.restore_selection()
        self.assertItemsEqual(self.ig.hidden_vertices, [ ], "vertices are hidden after restore")

    def test_hide_and_restore_complement(self):

        self.ig.do_press_action(0)
        self.ig.do_press_action(1)
        self.ig.do_press_action(2)
        self.selection.hide_complement()
        self.assertItemsEqual(self.ig.hidden_vertices, [ 3, 4, 5 ], "selection complement is not hidden")
        self.selection.restore_complement()
        self.assertItemsEqual(self.ig.hidden_vertices, [ ], "vertices are hidden after restore")

    def test_deselect_all(self):

        self.ig.do_press_action(0)
        self.ig.do_press_action(1)
        self.ig.do_press_action(2)
        self.selection.deselect_all()
        self.assertItemsEqual(self.selection.get_selection(), [ ], "selection contains vertices")
        self.assertItemsEqual(self.ig.visible_vertices, [ 0, 1, 2, 3, 4, 5 ], "vertices are hidden")

