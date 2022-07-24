'''
Provide the TSP Solver class.
'''
from matplotlib import pyplot as plt
from matplotlib import collections as mc

from shared.interfaces import SolutionProtocol, Solver, TSPSolution
from tsp import TSP

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

    def solve(self, problem: TSP, solution_protocol: SolutionProtocol) -> None:
        '''Solve and plot'''
        starting_sol = problem.path
        starting_cost = problem.cost(starting_sol)

        best_sol, best_cost = solution_protocol.search(problem, starting_sol)

        self._plot_points(problem, starting_sol, starting_cost)
        self._plot_points(problem, best_sol, best_cost)
        plt.show()
