import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable, Divider, Size

class GraphContainer(object):

    def __init__(self, graph):

        self._graph = graph
        divider = make_axes_locatable(graph.ax)
        self._menu = divider.append_axes("right", size = 2.0, pad = 0.1)
        self._menu.tick_params(left = False, labelleft = False, bottom = False, labelbottom = False)

        
