'''
Provide the Travelling Salesman Problem class.
'''
from typing import List, Tuple
import numpy as np
from collections import defaultdict

from shared.interfaces import Problem, Solution, Path
from tsp_solution import TSPSolution

class TSP(Problem):
    def __init__(self, N: int) -> None:
        super().__init__()
        self.N = N # number of cities
        self.cities = np.random.rand(N, 2) # coordinates of cities

    def _edge_distance(self, i, j) -> float:
        return np.sqrt(np.sum(np.power(self.cities[i, :] - self.cities[j, :], 2)))

    def cost(self, path: Path) -> float:
        '''Return the Euclidean distance if the path is followed.'''
        shifted_cities = np.vstack((self.cities[path[1:], :], self.cities[path[0], :]))
        differences = np.power(self.cities[path] - shifted_cities, 2)
        cost = np.sum(np.sqrt(differences[:, 0] + differences[:, 1]))

        return cost

    def _get_path_runs(self, path: Path, length: int) ->  List[int]:
        '''Generator for consecutive runs of a path'''
        runs = []
        for i in range(self.N):
            if i <= self.N - length:
                runs.append(path[i:(i + length)])
            else:
                # looping back around
                runs.append([*path[i:], *path[:(self.N - length + i)]])

        return runs

    def _two_opt_swap(self, path: Path, v1: int, v2: int):
        '''2-opt swap'''
        return [*path[:v1 + 1], *path[v2:v1:-1], *path[v2 + 1:]]

    def _find_neighbors_k_opt(self, path: Path, **kwargs) -> List[Path]:
        k = kwargs['k'] if 'k' in kwargs else 2

        if k != 2:
            raise NotImplementedError('Only 2-opt optimization supported.')
        
        neighbors = []
        
        for v1 in range(self.N):
            for v2 in range(v1 + 2, self.N):
                neighbors.append(self._two_opt_swap(path, v1, v2))
        
        return neighbors
        

    def find_neighbors(self, path: Path, method: str = 'opt', **kwargs) -> List[Path]:
        '''
        Find the neighbors of a solution.

        type corresponds to how we define a neighbor.
        - opt is related to k-opt optimization. For now, only 2-opt is implemented.
        '''
        if method == 'opt':
            return self._find_neighbors_k_opt(path, **kwargs)
        else:
            raise NotImplementedError('Only k-opt optimization supported.')

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
        sol = TSPSolution(self.N)

        # For the rest of the cities
        for _ in range(1, self.N):
            distances = np.sqrt(np.sum(np.power(self.cities - self.cities[path[-1], :], 2), 1))
            closest = self._find_argmin_excluding(distances, path)
            path.append(closest)

        sol.set_path(path)

        return sol

    def _edges_to_path(self, path_edges: List[Tuple[int, int]]) -> TSPSolution:
        '''Takes a list of i, j tuples and turns it into a valid path'''
        sol = TSPSolution(self.N)
        path = [0]

        for _ in range(self.N - 1):
            # get previous node
            prev = path[-1]
            # get an edge that contains the node
            curr_edge = list(filter(lambda edge: prev in edge, path_edges))[0]
            # remove it from future consideration
            path_edges.remove(curr_edge)
            # add whichever node we haven't seen yet
            curr = curr_edge[0] if curr_edge[0] != prev else curr_edge[1]
            path.append(curr)

        sol.set_path(path)

        return sol

    def _union(self, parent, x, y):
        parent[x] = y

    def _find_parent(self, parent, i: int):
        '''Utility function for _detect_cycle to find the subset of element i'''
        if parent[i] == -1:
            # no further subsets, is its own subset
            return i
        else:
            return self._find_parent(parent, parent[i])

    def detect_cycle(self, path_edges: List[Tuple[int, int]]) -> bool:
        parent = [-1] * self.N

        # create mapping from i to j to store edges
        graph = defaultdict(list)
        for path in path_edges:
            i, j = path
            # add mapping for edge
            graph[i].append(j)

        # Iterate through all edges, find subset of both vertices
        # of every edge, if both subsets the same, there is a cycle
        for i in graph:
            for j in graph[i]:
                x = self._find_parent(parent, i)
                y = self._find_parent(parent, j)
                if x == y:
                    return True
                self._union(parent, x, y)

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

            # make sure path remains a path
            if degree[i] < 2 and degree[j] < 2:
                # make sure the path doesn't prematurely become a cycle
                # however, if the graph has degree 2 * N - 2, then the next edge will become a cycle
                if not self.detect_cycle([*path_edges, (i, j)]) or sum(degree) == self.N * 2 - 2:
                    path_edges.append((i, j))
                    degree[i] += 1
                    degree[j] += 1

        return self._edges_to_path(path_edges)
