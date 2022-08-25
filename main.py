'''
Travelling Salesman Problem with Tabu Search

Dawson Ren, July 15th, 2022
'''
from search import LocalSearch, TabuSearch
from tsp import TSP
from solver import TSPGreedySolver, TSPNNSolver, TSPSearchSolver
from utils.display import plot_points, display

if __name__ == '__main__':
    N = 50
    problem = TSP(N)

    tsp_nn = TSPNNSolver()

    # ts = TabuSearch()
    ls = LocalSearch()
    tsp_solver = TSPSearchSolver()

    tsp_greedy = TSPGreedySolver()

    # solution = tsp_solver.solve(problem, ts)
    solution = tsp_nn.solve(problem)
    solution2 = tsp_solver.solve(problem, ls)
    solution3 = tsp_greedy.solve(problem)

    plot_points(problem, solution, problem.cost(solution.path()), 'Nearest Neighbor')
    plot_points(problem, solution2, problem.cost(solution2.path()), 'Local Search on Greedy Edge')
    plot_points(problem, solution3, problem.cost(solution3.path()), 'Greedy Edge')
    display()
    
