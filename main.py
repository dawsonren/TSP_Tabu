'''
Travelling Salesman Problem with Tabu Search

Dawson Ren, July 15th, 2022
'''
from search import LocalSearch, TabuSearch
from tsp import TSP
from solver import TSPSolver
from utils.display import plot_points, display

if __name__ == '__main__':
    N = 100
    problem = TSP(N)

    solution_greedy = problem.greedy_path_heuristic_solution()

    ts = TabuSearch()
    ls = LocalSearch()
    tsp_solver = TSPSolver()
    solution = tsp_solver.solve(problem, ts, init_sol=solution_greedy.copy(), verbose=True)
    solution2 = tsp_solver.solve(problem, ls, init_sol=solution_greedy.copy(), verbose=True)

    plot_points(problem, solution_greedy, problem.cost(solution_greedy.path()), 'Greedy Edge')
    plot_points(problem, solution, problem.cost(solution.path()), 'Tabu Search on Greedy Edge')
    plot_points(problem, solution2, problem.cost(solution2.path()), 'Local Search on Greedy Edge')
    display()
    
