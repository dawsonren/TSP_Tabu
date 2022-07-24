'''
Travelling Salesman Problem with Tabu Search

Dawson Ren, July 15th, 2022
'''
import search
import tsp
import solver
from utils.timer import timer

@timer
def main():
    N = 30
    problem = tsp.TSP(N)

    ls = search.LocalSearch()
    tsp_solver = solver.TSPSolver()

    tsp_solver.solve(problem, ls)

if __name__ == '__main__':
    main()
    
