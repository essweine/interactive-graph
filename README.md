# Interactive graph viewer for matplotlib

## Example

```
import matplotlib.pyplot as plt
from interactive_graph.graph import InteractiveGraph
fig, ax = plt.subplots()
ig = InteractiveGraph(ax)

vprops = { "radius": 0.01, "color": (0.0, 0.6, 0.8) }
for vid, xy in enumerate(np.random.rand(10, 2)):
    ig.add_vertex(vid, xy, label = "vertex {n}".format(n = idx), **vprops)

eprops = { "color": (0.0, 0.0, 0.0), "lw": 0.1 }
for eid, (v1, v2) in enumerate(zip(np.random.randint(0, 10, 25), np.random.randint(0, 10, 25))):
    ig.add_edge(eid, v1, v2, **eprops)
```

Hover over a vertex to see the label.  Click to drag.

Use to rescale axes to data limits:

```
ig.reset_view()
```

## About

I use [graph_tool](https://graph-tool.skewed.de) for graph analysis, but the graph viewer segfaults because there is something wrong with my GTK installation.  This was easier to put together than trying to solve that problem.
