'''
Travelling Salesman Problem with Tabu Search

Dawson Ren, July 15th, 2022
'''
from tsp import TSP, LocalSearch, TabuSearch, TSPSolver

if __name__ == '__main__':
    N = 30
    tsp = TSP(N)
    ls = LocalSearch()
    ts = TabuSearch()
    solver = TSPSolver()

    solver.solve(tsp, ls)
    tsp.path = list(range(30))
    solver.solve(tsp, ts)
