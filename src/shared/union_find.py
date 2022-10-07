'''
Extremely simple union find.
'''

class UnionFind():
    def __init__(self, size: int) -> None:
        self._parent = [-1] * size

    def union(self, x: int, y: int) -> None:
        self._parent[x] = y

    def find_parent(self, i: int) -> int:
        '''Utility function for _detect_cycle to find the subset of element i'''
        if self._parent[i] == -1:
            # no further subsets, is its own subset
            return i
        else:
            return self.find_parent(self._parent[i])