'''
Consider n different points in the unit square.

First of all, what is the distribution of the lengths of the edges?
Second of all, what is the probability that an edge of a given length is on the optimal TSP path?
What about a k-opt locally optimal path?
'''
import numpy as np
from matplotlib import pyplot as plt

from shared.interfaces import Problem, Solver
from tsp.solver import TSPHeldKarpSolver

def length_distribution(N: int) -> np.ndarray:
    points = np.random.rand(N, 2)
    shifted_cities = np.vstack((points[1:, :], points[0, :]))
    differences = np.power(points - shifted_cities, 2)
    return np.sqrt(differences[:, 0] + differences[:, 1])

def optimal_solve(problem: Problem, solver: Solver):
    return solver.solve(problem)

def main():
    plt.plot(length_distribution(100))

if __name__ == '__main__':
    main()
