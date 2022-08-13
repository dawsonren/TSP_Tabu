'''
Provide the Travelling Salesman Problem class.
'''
from typing import List, Tuple, Set
import numpy as np

from shared.interfaces import Problem, TSPSolution

class TSP(Problem):
    def __init__(self, N) -> None:
        super().__init__()
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
    
    def _interpolations(self, a, b) -> Set[Tuple[int, ...]]:
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

    def find_neighbors(self, path: TSPSolution) -> List[TSPSolution]:
        # TODO: Find a more computationally efficient definition of neighbor.
        return self._first_find_neighbors(path)

    def _find_argmin_excluding(self, lst, excluding) -> int:
        # set to initial value that's not in excluding
        argmin = list(set(range(len(lst))) - set(excluding))[0]
        min = lst[argmin]

        for i, l in enumerate(lst):
            if l < min and i not in excluding:
                min = l
                argmin = i
        
        return argmin

    def nearest_neighbor_heuristic_solution(self) -> TSPSolution:
        '''Uses the nearest neighbor heuristic to find an approximate solution'''
        path = [0]

        # For the rest of the cities
        for _ in range(1, self.N):
            distances = np.sqrt(np.sum(np.power(self.cities - self.cities[path[-1], :], 2), 1))
            closest = self._find_argmin_excluding(distances, path)
            path.append(closest)

        return path

    def _edges_to_path(self, path_edges: List[Tuple[int, int]]) -> TSPSolution:
        '''Takes a list of i, j tuples and turns it into a valid path'''
        path = [0]

        for _ in range(self.N - 1):
            # get previous node
            prev = path[-1]
            print(prev)
            # get an edge that contains the node
            curr_edge = list(filter(lambda edge: prev in edge, path_edges))[0]
            print(curr_edge)
            # remove it from future consideration
            path_edges.remove(curr_edge)
            # add whichever node we haven't seen yet
            curr = curr_edge[0] if curr_edge[0] != prev else curr_edge[1]
            path.append(curr)
            print(path)

        return self._reformat_path(path)

    def _detect_cycle(self, path_edges: List[Tuple[int, int]]) -> bool:
        '''Detects a cycle using path edges'''
        seen = set(path_edges[0])

        # this doesn't work :()

        for edge in path_edges[1:]:
            i, j = edge
            if i in seen and j in seen:
                return True

        return False


    def greedy_path_heuristic_solution(self) -> TSPSolution:
        '''Enumerates all posible paths and chooses the shortest ones greedily'''
        # Holds tuples of index i to index j, then their cost
        edge_distances: List[int, int, float] = []

        # collect all edges
        for i in range(self.N):
            for j in range(i + 1, self.N):
                edge_distances.append((i, j, self._edge_distance(i, j)))

        # sort by distance
        sorted_edge_distances = sorted(edge_distances, key=lambda x: x[2])

        degree = [0] * self.N # needs to be two for all nodes to be a path
        path_edges = []

        # greedily add to solution
        for edge in sorted_edge_distances:
            # check if path already fully connected
            if all([d == 2 for d in degree]):
                break

            i, j, _ = edge

            # if it won't break the path conditions, namely no node degrees > 2 and no cycles
            if degree[i] < 2 and degree[j] < 2 and not self._detect_cycle([*path_edges, (i, j)]):
                path_edges.append((i, j))
                degree[i] += 1
                degree[j] += 1

        return self._edges_to_path(path_edges)
