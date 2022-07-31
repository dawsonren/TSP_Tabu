'''
Provide the TSP Solver class.
'''
from matplotlib import pyplot as plt
from matplotlib import collections as mc

from shared.interfaces import SolutionProtocol, Solver, TSPSolution
from tsp import TSP

class TSPSolver(Solver):
    def __init__(self) -> None:
        super().__init__()

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

    def solve(self, problem: TSP, solution_protocol: SolutionProtocol) -> None:
        '''Solve the system and store in the class'''
        self.problem = problem
        self.starting_sol, self.starting_cost = problem.path, problem.cost(problem.path)
        self.best_sol, self.best_cost = solution_protocol.search(problem, problem.path)

    def display(self):
        '''Display the starting and best solutions. Must be called after solve()'''
        self._plot_points(self.problem, self.starting_sol, self.starting_cost)
        self._plot_points(self.problem, self.best_sol, self.best_cost)
        plt.show()

