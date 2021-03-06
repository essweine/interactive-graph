from random import choice
import matplotlib.pyplot as plt
import matplotlib.colors as mplcolors
from interactive_graph.graph import InteractiveGraph
from interactive_graph.container import GraphContainer
from interactive_graph.selection import Selection
from interactive_graph.selection_options import SelectionOptions

fig, ax = plt.subplots()

# This is the graph
ig = InteractiveGraph(ax)

# Add some additional functionality (vertex groups with a legend, and the ability to select by groups)
sel = Selection(ig, { "ec": (0.0, 0.0, 0.0) })
ig.add_press_action("select/deselect", sel.select_or_deselect)
sel_opts = SelectionOptions(sel) 
leg = sel_opts.create_legend()

n_groups = 10
n_vx = n_groups * 4
n_edges = n_vx * 3

# Assign each group a random color, and set the edge to a black outline when selected
groups = [ set() for n in range(n_groups) ]
vprops, sprops = [ ], [ ]
for n in range(n_groups):
    c = choice(list(mplcolors.CSS4_COLORS.keys()))
    vprops.append({ "radius": 0.01, "color": mcolors.to_rgba(c, 0.6) })
    sprops.append({ "radius": 0.01, "ec": (0.0, 0.0, 0.0) })

# Add some vertices and edges
for group, props in zip(groups, vprops):
    ig.add_vertices([ vxid for idx, vxid in enumerate(vx) if idx in group ], **props)

vx, edges = [ ], [ ]
for idx, xy in enumerate(np.random.rand(n_vx, 2)):
    vx.append((idx, xy, "vertex {n}".format(n = idx)))
    groups[idx % n_groups].add(idx)

eprops = { "color": (0.0, 0.0, 0.0), "lw": 0.1 }
for idx, (v1, v2) in enumerate(zip(np.random.randint(0, n_vx, n_edges), np.random.randint(0, n_vx, n_edges))):
    edges.append((len(edges), v1, v2))
ig.add_edges(edges, **eprops)

# Build the legend
for g in zip([ "group %d" % n for n in range(n_groups) ], groups, vprops, sprops):
    leg.add_group(*g)
leg.build()

gc = GraphContainer(ax, ig, sel_opts)

