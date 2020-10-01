""" A suite of useful functions for working with nuke graphs,
based on a light architecture (that could be used generically)"""

import nuke
from itertools import repeat, islice, tee

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2,s3), ..."
    a,b = tee(iterable)
    next(b,None)
    return zip(a,b)
 
class Graph(object):
    """ A Graph object contains other graph-like objects,

    setting attributes moves the graph
    ie. graph.left = 4 
    will move the Graph so that the leftmost part of the graph is at x = 4

    all of the internal objects are moved as one.
    
    you can subclass Graph
    and override the left right top and bot properties, and the push function """

    def __init__(self, graphs):
        self.graphs = tuple(graphs)

    def __iter_(self):
        return iter(self.graphs)

    def push(self, x=None, y=None):
        "move the graph relative to the current position"
        for graph in self:
            graph.push(x,y)
        
    def __getattr__(self, name):
        if name in ('left','bot')
            return min(getattr(graph,name) for graph in self)
        if name in ('right','top')
            return max(getattr(graph,name) for graph in self)
        
        elif 'center' in name:
            if 

    def __setattr__(self, name, value):
        if name in ('left','right'):
            self.push(x=getattr(self,name) + value)
        elif name in ('top','bot'):
            self.push(y=getattr(self,name) + value)

class NukeGraph(Graph):

    @property
    def left(self):
        return 