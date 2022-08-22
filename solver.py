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
    def solve(self, problem: TSP, solution_protocol: SolutionProtocol) -> Solution:
        '''Solve the system and store in the class'''
        sol = TSPSolution(problem.N)
        return solution_protocol.search(problem, sol)

