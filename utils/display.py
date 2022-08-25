'''
Provide plotting functionality for TSP Solutions
'''
from matplotlib import pyplot as plt
from matplotlib import collections as mc
from shared.interfaces import Problem, Solution


def plot_points(problem: Problem, solution: Solution, cost: float, strategy: str = '') -> None:
        '''Plot the points of a given solution'''
        points = problem.cities[solution.path()].tolist()
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
        ax.set_title(f'Strategy: {strategy}, Cost: {cost}')
        
def display():
        plt.show()