'''
Consider n different points in the unit square.

First of all, what is the distribution of the lengths of the edges?
Second of all, what is the probability that an edge of a given length is on the optimal TSP path?
What about a k-opt locally optimal path?
'''
from typing import List
import numpy as np
from matplotlib import pyplot as plt
import scipy.integrate as integrate

from shared.interfaces import Problem, Solver
from utils.display import plot_basic
from tsp.tsp import TSP
from utils.display import display, plot_path_length_histogram
from tsp.solver import TSPHeldKarpSolver

# integration/differentiation resolution for theoretical distribution
H = 0.001

def get_distances(points: np.ndarray) -> np.ndarray:
    shifted_cities = np.vstack((points[1:, :], points[0, :]))
    differences = np.power(points - shifted_cities, 2)
    return np.sqrt(differences[:, 0] + differences[:, 1])

def differentiate(array: np.ndarray) -> np.ndarray:
    return (array[1:] - array[:-1]) / H

def cdf_theoretical_greater_than_1(t: np.float64) -> List[int]:
    return integrate.quad(lambda x: 4 * (1 - x) * (1 - (1 / 2) * min(1, np.sqrt(t ** 2 - x ** 2))) * min(1, np.sqrt(t ** 2 - x ** 2)), 0, 1)

def theoretical_distribution() -> np.ndarray:
    # let a, b = 1 so we're in the unit square
    x1 = np.arange(0, 1, H)
    # got this article from an academic journal, two different cases for pdf
    # one part for less than one, another for greater than one
    # the derivation is complex!
    # https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&ved=2ahUKEwiuj9mPncj6AhULrokEHVhPDSU4ChAWegQIBBAB&url=https%3A%2F%2Fwww.mdpi.com%2F2571-905X%2F3%2F1%2F1%2Fpdf&usg=AOvVaw2AXLhx9PJm9ZKGaGu_4Sy0
    fx1 = x1 * 2 * (np.power(x1, 2) - 4 * x1 + np.pi)
    x2 = np.arange(1, np.sqrt(2), H)
    # TODO: I'm sure the fundamental theorem of calculus can eliminate both integration and differentiation
    # but I'm worried about the change of variables since the upper integration limit is a min function
    # numerical integration
    Fx2 = [cdf_theoretical_greater_than_1(t) for t in x2]
    Fx2 = np.array([start - end for start, end in Fx2])
    # numerical differentiation
    fx2 = differentiate(Fx2)
    # remove last because we lose one from inner difference, so differentiate by left side
    return np.concatenate((x1, x2[:-1])), np.concatenate((fx1, fx2))

def length_distribution(N: int) -> np.ndarray:
    points = np.random.rand(N, 2)
    return get_distances(points)

def repeat_many_distributions(N: int, total: int) -> np.ndarray:
    return np.concatenate(tuple([length_distribution(N) for _ in range(int(total / N))]), axis=0)

def optimal_solve(problem: Problem, solver: Solver):
    return solver.solve(problem)

def produce_path_distributions(total: int) -> np.ndarray:
    hk_size = 10
    solver = TSPHeldKarpSolver()
    tsps = [TSP(hk_size) for _ in range(int(total / hk_size))]
    paths = [solver.solve(tsp).path() for tsp in tsps]
    distances = [get_distances(tsp.cities[path]) for tsp, path in zip(tsps, paths)]
    return np.concatenate(distances)

def main():
    plot_path_length_histogram(length_distribution(100000))
    plot_basic(*theoretical_distribution(), title='Theoretical Distribution for Distances Between Two Points in the Unit Square')
    
    display()

if __name__ == '__main__':
    main()
