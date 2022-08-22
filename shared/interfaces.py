'''
Interfaces that we use in the project.

TSPSolution is a valid solution type.
Problem is meant to be consumed by a SolutionProtocol.
SolutionProtocol is driven by a Solver.
Solver is the highest level of abstraction.
'''
from abc import ABC, abstractmethod
from typing import List

Path = List[int]

class Solution(ABC):
    @property
    @abstractmethod
    def path(self) -> Path:
        '''Provide the path'''
        pass

    @path.setter
    @abstractmethod
    def set_path(self, path: Path) -> None:
        '''Sets the path. INVARIANT - contains any permutation of 0 to N - 1,
        with N being the number of cities.'''
        pass

class Problem(ABC):
    @abstractmethod
    def find_neighbors(self, solution: Path) -> List[Path]:
        '''Find neighbor solutions.'''
        pass

    @abstractmethod
    def cost(self, solution: Path) -> float:
        '''Determine cost of solution. Lower is better.'''
        pass

class SolutionProtocol(ABC):
    @abstractmethod
    def stoppingCondition(self) -> bool:
        pass

    @abstractmethod
    def search(self, problem: Problem, starting_solution: Solution) -> Solution:
        pass

class Solver(ABC):
    @abstractmethod
    def solve(self, problem: Problem, solution_protocol: SolutionProtocol):
        pass
