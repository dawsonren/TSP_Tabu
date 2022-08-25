'''
Provide the TSP Solver classes.

TSPSearchSolver - Use a SearchProtocol to find a locally optimal solution.
TSPNNSolver - Use the nearest neighbor heuristic to find an approximate solution.
TSPGreedySolver - Use the greedy edge algorithm to find an approximate solution.
TSPChristofidesSolver - Use the Christofides algorithm to find an approximate solution.
'''
from collections import defaultdict
from typing import List, Tuple
import numpy as np

from shared.interfaces import SearchProtocol, Solver, Solution
from tsp_solution import TSPSolution
from tsp import TSP
from utils.timer import timer


class TSPSearchSolver(Solver):
    @timer
    def solve(self, problem: TSP, search_protocol: SearchProtocol, init_sol: Solution = None, verbose = False) -> Solution:
        '''Solve the system and store in the class'''
        init_sol = TSPSolution(problem.N) if init_sol is None else init_sol
        return search_protocol.search(problem, init_sol, verbose)

class TSPNNSolver(Solver):
    def _find_argmin_excluding(self, lst, excluding) -> int:
        # set to initial value that's not in excluding
        argmin = list(set(range(len(lst))) - set(excluding))[0]
        min = lst[argmin]

        for i, l in enumerate(lst):
            if l < min and i not in excluding:
                min = l
                argmin = i
        
        return argmin

    @timer
    def solve(self, problem: TSP, verbose = False) -> Solution:
        '''Uses the nearest neighbor heuristic to find an approximate solution'''
        path = [0]
        if verbose:
            print('Starting nearest neighbor search at node 0.')
        sol = TSPSolution(problem.N)

        # For the rest of the cities
        for _ in range(1, problem.N):
            distances = np.sqrt(np.sum(np.power(problem.cities - problem.cities[path[-1], :], 2), 1))
            closest = self._find_argmin_excluding(distances, path)
            if verbose:
                print(f'Next closest neighbor is {closest}.')
            path.append(closest)

        sol.set_path(path)

        return sol

class TSPGreedySolver(Solver):
    def _edges_to_path(self, N: int, path_edges: List[Tuple[int, int]]) -> Solution:
        '''Takes a list of i, j tuples and turns it into a valid path'''
        sol = TSPSolution(N)
        path = [0]

        for _ in range(N - 1):
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
    
    def _union(self, parent: List[int], x: int, y: int) -> None:
        parent[x] = y

    def _find_parent(self, parent: List[int], i: int) -> int:
        '''Utility function for _detect_cycle to find the subset of element i'''
        if parent[i] == -1:
            # no further subsets, is its own subset
            return i
        else:
            return self._find_parent(parent, parent[i])

    def _detect_cycle(self, N: int, path_edges: List[Tuple[int, int]]) -> bool:
        parent = [-1] * N

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
    
    @timer
    def solve(self, problem: TSP, verbose = False) -> Solution:
        '''Enumerates all posible paths and chooses the shortest ones greedily'''
        # Holds tuples of index i to index j, then their cost
        edge_distances: List[int, int, float] = []

        # collect all edges
        for i in range(problem.N):
            for j in range(i + 1, problem.N):
                edge_distances.append((i, j, problem.edge_distance(i, j)))

        # sort by distance
        sorted_edge_distances = sorted(edge_distances, key=lambda x: x[2])

        if verbose:
            print('Starting greedy edge construction. Shortest and longest edges shown below.')
            print(f'Shortest edge: {sorted_edge_distances[0]}')
            print(f'Longest edge: {sorted_edge_distances[-1]}')

        degree = [0] * problem.N # needs to be two for all nodes to be a path
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
                if not self._detect_cycle(problem.N, [*path_edges, (i, j)]) or sum(degree) == problem.N * 2 - 2:
                    if verbose:
                        print(f'Add edge {i} <-> {j}')
                    path_edges.append((i, j))
                    degree[i] += 1
                    degree[j] += 1

        return self._edges_to_path(problem.N, path_edges)

class TSPChristofidesSolver(Solver):
    @timer
    def solve(self, problem: TSP, verbose = False) -> Solution:
        '''Provide solution using algorithm of Christofides'''

        # TODO: write my own MultiGraph class (omg...)

        # create minimum spanning tree using Kruskal's algorithm
        # find vertices of odd degree
        # find minimum-weigh perfect matching on the induced subgraph of vertices of odd degree
        # combine edges from MST and perfect matching to form a multigraph, where every node has even degree
        # form a eulerian circuit
        # convert into a hamiltonian circuit

        return TSPSolution(problem.N)

# TODO: check out asadpour - probabilistic determination!