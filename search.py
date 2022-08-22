'''
Provide the LocalSearch and TabuSearch classes.
'''
from collections import deque
import random
from typing import Tuple
from shared.interfaces import SolutionProtocol, Problem, Solution
from tsp_solution import TSPSolution

class LocalSearch(SolutionProtocol):
    def __init__(self) -> None:
        self.max_iter = 50
        self.iters = 0

    def stoppingCondition(self) -> bool:
        return self.iters > self.max_iter

    def search(self, problem: Problem, starting_solution: Solution) -> Solution:
        best_path = starting_solution.path()
        best_candidate = starting_solution.path()
        while not self.stoppingCondition():
            self.iters += 1
            neighborhood = problem.find_neighbors(best_path)
            best_candidate = neighborhood[0]

            for candidate in neighborhood:
                if problem.cost(candidate) < problem.cost(best_candidate):
                    best_candidate = candidate
            
            if problem.cost(best_candidate) < problem.cost(best_path):
                best_path = best_candidate
                print(f'Solution was improved! {best_path}')
            else:
                print('Stuck in a local minima...')
                break
        
        starting_solution.set_path(best_path)
        return starting_solution


class TabuSearch(SolutionProtocol):
    def __init__(self) -> None:
        super().__init__()
        self.max_iter = 100
        self.iters = 0
        self.max_tabu_size = 1000

    def stoppingCondition(self) -> bool:
        return self.iters > self.max_iter

    def search(self, problem: Problem, starting_solution: Solution) -> Solution:
        best_path = starting_solution.path()
        best_candidate = starting_solution.path()
        tabu_list = deque([starting_solution], self.max_tabu_size)

        while not self.stoppingCondition():
            self.iters += 1
            neighborhood = problem.find_neighbors(best_path)
            best_candidate = random.sample(neighborhood, 1)[0]

            for candidate in neighborhood:
                if problem.cost(candidate) < problem.cost(best_candidate) and not candidate in tabu_list:
                    best_candidate = candidate
            
            if problem.cost(best_candidate) < problem.cost(best_path):
                best_sol = best_candidate
                print(f'Solution was improved! {best_sol}')
            
            tabu_list.append(best_candidate)

            if len(tabu_list) > self.max_tabu_size:
                tabu_list.popleft()

        starting_solution.set_path(best_sol)
        return starting_solution
