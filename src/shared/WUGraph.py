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
This scheme works best when the graph is relatively dense, as it is for the TSP.
"""
from typing import Iterator, List, Tuple
import numpy as np

class WUGraph:
    def __init__(self, size: int):
        '''Creates a WUGraph. size is the number of nodes.'''
        self._len = size
        self._adj_matrix = np.ndarray((size, size), np.float32)
        self._adj_matrix.fill(-1)
        self._cities = None

    def edge_distance(self, i, j) -> None:
        np.sqrt(np.sum(np.power(self._cities[i, :] - self._cities[j, :], 2)))

    def load_cities(self, cities: np.ndarray) -> None:
        '''Load cities, with N rows and 2 columns in Euclidean space.'''
        self._cities = cities
        for i in range(cities.shape[0]):
            for j in range(i + 1, cities.shape[0]):
                self.set_edge(i, j, self.edge_distance(i, j))

    def all_edges(self) -> Iterator[Tuple[int, int]]:
        '''Return all edges. Guaranteed that i < j.'''
        for i in range(self._len):
            for j in range(i + 1, self._len):
                if self.get_edge_exists(i, j):
                    yield i, j

    def set_edge(self, u: int, v: int, w: float) -> None:
        if u == v:
            raise Exception('WUGraph: cannot set self edge')
        self._adj_matrix[u, v] = w
        self._adj_matrix[v, u] = w

    def get_edge(self, u: int, v: int) -> float:
        if u == v:
            raise Exception('WUGraph: cannot get self edge')
        if self._adj_matrix[u, v] == -1:
            raise Exception(f'No edge exists between {u} and {v}')
        
        return self._adj_matrix[u, v]

    def get_edge_exists(self, u: int, v: int) -> bool:
        if u == v:
            raise Exception('WUGraph: cannot get self edge')
        return self._adj_matrix[u, v] != -1

    def get_degree(self, u: int) -> int:
        return np.sum(self._adj_matrix[u, :] != -1)

    def get_neighbors(self, u: int) -> List[int]:
        return np.where(self._adj_matrix[u, :] > 0)[0].tolist()

    def get_mst(self):
        '''Return another WUGraph with the Minimum Spanning Tree using Prim's Algorithm'''
        mst = WUGraph(self._len)

        # cheapest cost of connection
        C = self._len * [np.inf]
        # edge providing cheapest connection
        E = self._len * [None]
        # nodes to include
        Q = set(range(self._len))
        
        # relaxation time
        while len(Q) != 0:
            v = min(Q, key=lambda q: C[q])
            Q.remove(v)
            for w in self.get_neighbors(v):
                if w in Q and self.get_edge(v, w) < C[w]:
                    C[w] = self.get_edge(v, w)
                    E[w] = (v, w)

        # push into mst
        for edge in E:
            if edge is None: continue
            u, v = edge
            mst.set_edge(u, v, self.get_edge(u, v))

        return mst

    def __len__(self):
        return self._len
