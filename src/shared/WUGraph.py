"""
A weighted undirected graph implementation in pure python.

Graphs have nodes connected by edges. The edges have a "weight" attached to
them. We exclusively use natural numbers (including 0) to reference these
nodes. We also set the limitation that all present edges have positive float
values, and a -1 means that no edge exists.

We implement the following interface:
set_edge(u: int, v: int, w: float) -> None : sets weight w from node u to v.
get_edge(u: int, v: int) -> float : gets weight w from node u to v.
get_degree(u: int) -> int : gets degree of node u.

To keep track of the nodes and edges, we use an adjacency matrix implementation.
This scheme works best when the graph is relatively dense.
"""
from typing import Tuple
import numpy as np

class WUGraph:
    def __init__(self, size: int):
        '''Creates a WUGraph. size is the number of nodes.'''
        self.len = size
        self.adj_matrix = np.ndarray((size, size), np.float64)
        self.adj_matrix.fill(-1)

    def _opt_swap(self, u: int, v: int) -> Tuple[int, int]:
        return v, u if u > v else u, v

    def set_edge(self, u: int, v: int, w: float):
        u, v = self._opt_swap(u, v)
        self.adj_matrix[u, v] = w

    def get_edge(self, u: int, v: int):
        u, v = self._opt_swap(u, v)
        if self.adj_matrix[u, v] == -1:
            raise Exception(f'No edge exists between {u} and {v}')
        
        return self.adj_matrix[u, v]

    def get_degree(self, u: int):
        # TODO: Confirm this works properly
        return np.sum(self.adj_matrix[u, :] != -1)

    # TODO: Write get_neighbors

    def __len__(self):
        return self.len
