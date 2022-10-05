'''
Provide plotting functionality for TSP Solutions
'''
from matplotlib import pyplot as plt
from matplotlib import collections as mc
from shared.interfaces import SolutionWrapper, Problem, Solution
from matplotlib.axes import Axes
from matplotlib.collections import LineCollection

def get_line_collection(problem: Problem, solution: Solution, color: str) -> LineCollection:
    '''Get a line collection for a collection of points that represents the full Hamiltonian cycle.'''
    points = problem.cities[solution.path()].tolist()

    lines = []
    for start, end in zip(points, [*points[1:], points[0]]):
        lines.append([tuple(start), tuple(end)])

    line_collection = mc.LineCollection(lines, colors=[color])

    return line_collection

def get_points(problem: Problem, solution: Solution):
    points = problem.cities[solution.path()].tolist()
    x_vals, y_vals = zip(*points)
    return x_vals, y_vals

def plot_points(problem: Problem, sw: SolutionWrapper) -> None:
    _, ax = plt.subplots()
    ax.autoscale()
    ax.margins(0.1)
    ax.set_title(f'Strategy: {sw.strategy}, Cost: {sw.cost}')

    lc = get_line_collection(problem, sw.solution, 'r')
    x_vals, y_vals = get_points(problem, sw.solution)

    ax.add_collection(lc)
    ax.plot(x_vals, y_vals, color='r', marker='o')
    
def compare_plot_points(problem: Problem, sw1: SolutionWrapper, sw2: SolutionWrapper) -> None:
    '''Plot the solution of each DisplaySetting with the corresponding points from the Problem'''
    _, ax = plt.subplots()
    ax.autoscale()
    ax.margins(0.1)
    ax.set_title('Traveling Salesman Problem')

    lc1 = get_line_collection(problem, sw1.solution, 'r')
    lc2 = get_line_collection(problem, sw2.solution, 'b')

    # TODO: Figure out what's going on with the colors with lc1
    # TODO: Add legend

    x_vals, y_vals = get_points(problem, sw1.solution)

    ax.add_collection(lc1)
    ax.add_collection(lc2)

    ax.plot(x_vals, y_vals, color='k', marker='o')

    return ax

def plot_path_length_histogram():
    '''Given a problem, plot a histogram of all its path lengths.'''
    pass

def display():
    plt.show()