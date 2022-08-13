'''
Travelling Salesman Problem with Tabu Search

Dawson Ren, July 15th, 2022
'''
from search import LocalSearch
from tsp import TSP
from solver import TSPSolver
from utils.timer import timer
from display import plot_points, display

@timer
def solve(problem, ls, tsp_solver):
    return tsp_solver.solve(problem, ls)

if __name__ == '__main__':
    N = 30
    problem = TSP(N)

    solution = problem.greedy_path_heuristic_solution()

    # ls = LocalSearch()
    # tsp_solver = TSPSolver()
    # solution2 = solve(problem, ls, tsp_solver)

    plot_points(problem, solution, problem.cost(solution), 'Greedy Edge Search')
    # print(solution2)
    # plot_points(problem, solution2, problem.cost(solution2), 'Local Search w/ Interpolation')
    display()
    
