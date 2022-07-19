'''
Interfaces that we use in the project.

TSPSolution is a valid solution type.
Problem is meant to be consumed by a SolutionProtocol.
SolutionProtocol is driven by a Solver.
Solver is the highest level of abstraction.
'''
from abc import ABC, abstractmethod
from typing import List

TSPSolution = List[int]

class Problem(ABC):
    @abstractmethod
    def find_neighbors(self, solution):
        '''Find neighbor solutions.'''
        pass

    @abstractmethod
    def cost(self, solution):
        '''Determine cost of solution. Lower is better.'''
        pass

class SolutionProtocol(ABC):
    @abstractmethod
    def stoppingCondition(self) -> bool:
        pass

    @abstractmethod
    def search(self, problem: Problem, starting_solution):
        pass

class Solver(ABC):
    @abstractmethod
    def solve(self, problem: Problem, solution_protocol: SolutionProtocol):
        pass
