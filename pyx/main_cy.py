'''
Travelling Salesman Problem with Tabu Search

Dawson Ren, July 15th, 2022
'''
import pyximport; pyximport.install()
from search_cy import LocalSearch
from tsp_cy import TSP
from solver import TSPSolver
from utils.timer import timer

@timer
def solve(problem, ls, tsp_solver):
    tsp_solver.solve(problem, ls)

if __name__ == '__main__':
    N = 30
    problem = TSP(N)
    ls = LocalSearch()
    tsp_solver = TSPSolver()
    solve(problem, ls, tsp_solver)
    tsp_solver.display()
    

