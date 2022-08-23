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
    N = 20
    problem = TSP(N)

    solution_greedy = problem.greedy_path_heuristic_solution()

    ls = LocalSearch()
    tsp_solver = TSPSolver()
    solution2 = tsp_solver.solve(problem, ls, solution_greedy.copy())

    # plot_points(problem, solution_greedy, problem.cost(solution_greedy.path()), 'Greedy Edge')
    # print(solution2.path())
    # plot_points(problem, solution2, problem.cost(solution2.path()), 'Local Search on Greedy Edge')
    # display()
    
