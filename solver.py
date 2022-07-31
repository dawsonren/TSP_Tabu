'''
Provide the TSP Solver class.
'''
from typing import Tuple
from shared.interfaces import SolutionProtocol, Solver, TSPSolution
from tsp import TSP

class TSPSolver(Solver):
    def solve(self, problem: TSP, solution_protocol: SolutionProtocol) -> TSPSolution:
        '''Solve the system and store in the class'''
        return solution_protocol.search(problem, problem.path)

