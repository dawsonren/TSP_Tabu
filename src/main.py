'''
Travelling Salesman Problem with Tabu Search

Dawson Ren, July 15th, 2022
'''
from tsp.search import LocalSearch, TabuSearch
from shared.interfaces import SolutionWrapper
from tsp.tsp import TSP
from tsp.solver import TSPBruteForceSolver, TSPGreedySolver, TSPHeldKarpSolver, TSPNNSolver, TSPSearchSolver
from utils.display import plot_points, display, compare_plot_points

def main():
    N = 100
    problem = TSP(N)

    tsp_nn = TSPNNSolver()
    tsp_greedy = TSPGreedySolver()
    tsp_solver = TSPSearchSolver()
    ls = LocalSearch()
    ts = TabuSearch()

    solution1 = tsp_nn.solve(problem)
    solution2 = tsp_greedy.solve(problem)
    solution3 = tsp_solver.solve(problem, ls, init_sol=solution2.copy())
    # solution4 = tsp_solver.solve(problem, ts, init_sol=solution2.copy())
    
    plot_points(problem, SolutionWrapper(solution1, problem.cost(solution1.path()), 'Nearest Neighbor'))
    sw_ge = SolutionWrapper(solution2, problem.cost(solution2.path()), 'Greedy Edge')
    sw_ls = SolutionWrapper(solution3, problem.cost(solution3.path()), 'Local Search on Greedy Edge')
    plot_points(problem, sw_ge)
    plot_points(problem, sw_ls)
    # plot_points(problem, SolutionWrapper(solution4, problem.cost(solution4.path()), 'Tabu Search on Greedy Edge'))
    display()

def hk():
    N = 15
    problem = TSP(N)

    tsp_bf = TSPBruteForceSolver()
    tsp_hk = TSPHeldKarpSolver()

    # sol1 = tsp_bf.solve(problem)
    sol2 = tsp_hk.solve(problem)

    # sw_bf = SolutionWrapper(sol1, problem.cost(sol1.path()), 'Brute Force Search')
    sw_hk = SolutionWrapper(sol2, problem.cost(sol2.path()), 'Held-Karp Algorithm')

    # plot_points(problem, sw_bf)
    plot_points(problem, sw_hk)

    display()

if __name__ == '__main__':
    main()



    # TODO: Experiment - create 100 different TSPs and find the distribution of paths and the likelihood of being
    # in the optimal path. Is there any way we can model a probability distribution?
