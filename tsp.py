'''
Provide the TSP, TSPSolver, LocalSearch classes.
'''
from typing import List, Tuple, Set
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import collections as mc
from collections import deque
import random

from interfaces import Problem, SolutionProtocol, Solver

TSPSolution = List[int]

class TSP(Problem):
    def __init__(self, N) -> None:
        self.N = N # number of cities
        self.cities = np.random.rand(N, 2) # coordinates of cities
        self.path = list(range(N)) # Invariant - integers 0 to N - 1 appear exactly once

    def _edge_distance(self, i: int, j: int) -> float:
        '''Return the Euclidean distance between cities i and j'''
        x_i, y_i = self.cities[i, :]
        x_j, y_j = self.cities[j, :]
        return (x_i - x_j) ** 2 + (y_i - y_j) ** 2

    def cost(self, path: TSPSolution) -> float:
        '''Return the Euclidean distance if the path is followed'''
        total_dist = 0.0
        for i, j in zip(path, [*path[1:], 0]):
            total_dist += self._edge_distance(i, j)
        return total_dist

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


class LocalSearch(SolutionProtocol):
    def __init__(self) -> None:
        self.max_iter = 100
        self.iters = 0

    def stoppingCondition(self) -> bool:
        return self.iters > self.max_iter

    def search(self, problem: Problem, starting_solution) -> None:
        best_sol = starting_solution
        best_candidate = starting_solution
        while not self.stoppingCondition():
            self.iters += 1
            neighborhood = problem.find_neighbors(best_sol)
            best_candidate = neighborhood[0]

            for candidate in neighborhood:
                if problem.cost(candidate) < problem.cost(best_candidate):
                    best_candidate = candidate
            
            if problem.cost(best_candidate) < problem.cost(best_sol):
                best_sol = best_candidate
                print(f'Solution was improved! {best_sol}')
            else:
                print('Stuck in a local minima...')
                break
        
        return best_sol, problem.cost(best_sol)


class TabuSearch(SolutionProtocol):
    def __init__(self) -> None:
        self.max_iter = 100
        self.iters = 0
        self.max_tabu_size = 1000

    def stoppingCondition(self) -> bool:
        return self.iters > self.max_iter

    def search(self, problem: Problem, starting_solution) -> None:
        best_sol = starting_solution
        best_candidate = starting_solution
        tabu_list = deque([starting_solution], self.max_tabu_size)

        while not self.stoppingCondition():
            self.iters += 1
            neighborhood = problem.find_neighbors(best_sol)
            best_candidate = random.sample(neighborhood, 1)[0]

            for candidate in neighborhood:
                if problem.cost(candidate) < problem.cost(best_candidate) and not candidate in tabu_list:
                    best_candidate = candidate
            
            if problem.cost(best_candidate) < problem.cost(best_sol):
                best_sol = best_candidate
                print(f'Solution was improved! {best_sol}')
            
            tabu_list.append(best_candidate)

            if len(tabu_list) > self.max_tabu_size:
                tabu_list.popleft()

        return best_sol, problem.cost(best_sol)


class TSPSolver(Solver):
    def _plot_points(self, problem: TSP, solution: TSPSolution, cost: float):
        '''Plot the points of a given solution'''
        points = problem.cities[solution].tolist()
        x_vals, y_vals = zip(*points)

        lines = []
        for start, end in zip(points, [*points[1:], points[0]]):
            lines.append([tuple(start), tuple(end)])

        line_collection = mc.LineCollection(lines, colors=['r' for _ in range(8)])
        fig, ax = plt.subplots()
        ax.add_collection(line_collection)
        ax.plot(x_vals, y_vals, color='red', marker='o')
        ax.autoscale()
        ax.margins(0.1)
        ax.set_title(f'Cost: {cost}')

    def solve(self, problem: TSP, solution_protocol: LocalSearch) -> None:
        '''Solve and plot'''
        starting_sol = problem.path
        starting_cost = problem.cost(starting_sol)

        best_sol, best_cost = solution_protocol.search(problem, starting_sol)

        self._plot_points(problem, starting_sol, starting_cost)
        self._plot_points(problem, best_sol, best_cost)
        plt.show()




