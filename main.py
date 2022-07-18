'''
Travelling Salesman Problem with Tabu Search

Dawson Ren, July 15th, 2022
'''
from tsp import TSP, LocalSearch, TSPSolver

if __name__ == '__main__':
    tsp = TSP(20)
    ls = LocalSearch()
    solver = TSPSolver()

    solver.solve(tsp, ls)
