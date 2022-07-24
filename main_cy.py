'''
Travelling Salesman Problem with Tabu Search

Dawson Ren, July 15th, 2022
'''
import pyximport; pyximport.install()
import cython.search_cy
import cython.tsp_cy
from solver import TSPSolver

if __name__ == '__main__':
    N = 30
    tsp = tsp_cy.TSP(N)

    ls = search_cy.LocalSearch()
    ts = search_cy.TabuSearch()
    solver = TSPSolver()

    solver.solve(tsp, ls)
    tsp.path = list(range(N))
    solver.solve(tsp, ts)
    
