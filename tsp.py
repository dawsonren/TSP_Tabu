'''
Provide the Travelling Salesman Problem class.
'''
from typing import List, Tuple, Set
import numpy as np

from shared.interfaces import Problem, TSPSolution

class TSP(Problem):
    def __init__(self, N) -> None:
        self.N = N # number of cities
        self.cities = np.random.rand(N, 2) # coordinates of cities
        # Invariant - integers 0 to N - 1 appear exactly once in the path
        self.path = list(range(N)) 
    def _edge_distance(self, i: int, j: int) -> float:
        '''Return the Euclidean distance between cities i and j'''
        x_i, y_i = self.cities[i, :]
        x_j, y_j = self.cities[j, :]
        return np.sqrt((x_i - x_j) ** 2 + (y_i - y_j) ** 2)

    def _slow_cost(self, path: TSPSolution) -> float:
        '''Return the Euclidean distance if the path is followed, but unvectorized.'''
        total_dist = 0.0
        for i, j in zip(path, [*path[1:], path[0]]):
            total_dist += self._edge_distance(i, j)
        return total_dist

    def cost(self, path: TSPSolution) -> float:
        '''Return the Euclidean distance if the path is followed, but vectorized.'''
        shifted_cities = np.vstack((self.cities[path[1:], :], self.cities[path[0], :]))
        differences = np.power(self.cities[path] - shifted_cities, 2)
        cost = np.sum(np.sqrt(differences[:, 0] + differences[:, 1]))

        return cost

    def _find_city_neighbors(self, n) -> Tuple[int, int]:
        '''Find adjacent neighbors to n'''
        i = self.path.index(n)
        return self.path[(i - 1) % self.N], self.path[(i + 1) % self.N]

    def _ensure_order_and_provide_indices(self, a, b) -> Tuple[int, int, int, int]:
        '''Swap a and b if index(b) < index(a), and return their indices'''
        index_a = self.path.index(a)
        index_b = self.path.index(b)
        return (b, a, index_b, index_a) if index_b < index_a else (a, b, index_a, index_b)

    def _reformat_path(self, path) -> TSPSolution:
        '''Reformat path so that 0 is the first entry'''
        i = path.index(0)
        return [*path[i:], *path[:i]]
    
    def _interpolations(self, a, b) -> Set[TSPSolution]:
        '''
        Return a set of tuples with all interpolations of cities a and b.
        '''
        a, b, index_a, index_b = self._ensure_order_and_provide_indices(a, b)

        # get path between a and b excluding them
        path_1 = self.path[(index_a + 1):index_b]
        # get part of path that isn't path_1
        path_2 = [*self.path[0:(index_a + 1)], *self.path[index_b:]]

        interpolations = set()

        for i in range(len(path_1)):
            interp = self._reformat_path([*path_2[:i], *path_1, *path_2[i:]])
            interpolations.add(tuple(interp))

        for j in range(len(path_2)):
            interp = self._reformat_path([*path_1[:j], *path_2, *path_1[j:]])
            interpolations.add(tuple(interp))

        return interpolations

    def _first_find_neighbors(self, path) -> List[TSPSolution]:
        '''
        A neighbor of a path is another path that is 'closely related'.
        We construct a 'closely related' path where a sequence in the path
        is inserted between any of the elements of the remaining elements
        in the path.

        This results in a poor choice of neighbors, and finds many repeats (75% are repeated).
        '''
        self.path = path
        all_cities = set(path)
        all_interpolations = set()
        for a in all_cities:
            i, k = self._find_city_neighbors(a)
            for j in all_cities.difference(set([a, i, k])):
                # j is a new neighbor to i
                all_interpolations |= self._interpolations(i, j)
                
        return [list(interp) for interp in all_interpolations]

    def find_neighbors(self, path):
        # TODO: Find a more computationally efficient definition of neighbor.
        return self._first_find_neighbors(path)

    def nearest_neighbor_heuristic_solution(self):
        pass
