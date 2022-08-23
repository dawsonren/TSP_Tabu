'''
Provide the TSP Solver classes.
'''
from typing import Tuple
from shared.interfaces import SolutionProtocol, Solver, Solution
from tsp_solution import TSPSolution
from tsp import TSP
from utils.timer import timer

class TSPSolver(Solver):
    @timer
    def solve(self, problem: TSP, solution_protocol: SolutionProtocol, init_sol: TSPSolution = None) -> Solution:
        '''Solve the system and store in the class'''
        if init_sol is None:
            init_sol = TSPSolution(problem.N)
        return solution_protocol.search(problem, init_sol)

