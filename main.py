'''
Travelling Salesman Problem with Tabu Search

Dawson Ren, July 15th, 2022
'''
from search import LocalSearch
from tsp import TSP
from solver import TSPSolver
from utils.timer import timer
from display import plot_points, display

if __name__ == '__main__':
    N = 50
    problem = TSP(N)

    solution_greedy = problem.greedy_path_heuristic_solution()
    solution_nn = problem.nearest_neighbor_heuristic_solution()

    # ls = LocalSearch()
    # tsp_solver = TSPSolver()
    # solution2 = tsp_solver.solve(problem, ls)

    plot_points(problem, solution_greedy, problem.cost(solution_greedy.path()), 'Greedy Edge')
    plot_points(problem, solution_nn, problem.cost(solution_nn.path()), 'Nearest Neighbor')
    # print(solution2)
    # plot_points(problem, solution2, problem.cost(solution2), 'Local Search w/ Interpolation')
    display()
    
