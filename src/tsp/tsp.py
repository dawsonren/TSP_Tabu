'''
Provide the Travelling Salesman Problem class.
'''
from typing import List
import numpy as np
import pyximport
pyximport.install()

from shared.interfaces import Problem, Path
import cost.cost as ccost # C cost, colloquially

class TSP(Problem):
    def __init__(self, N: int) -> None:
        super().__init__()
        self.N = N # number of cities
        self.cities = np.random.rand(N, 2) # coordinates of cities

    def edge_distance(self, i, j) -> float:
        return np.sqrt(np.sum(np.power(self.cities[i, :] - self.cities[j, :], 2)))

    def _python_cost(self, path: Path) -> float:
        '''Kept here as a reminder of functionality, do not use'''
        shifted_cities = np.vstack((self.cities[path[1:], :], self.cities[path[0], :]))
        differences = np.power(self.cities[path] - shifted_cities, 2)
        cost = np.sum(np.sqrt(differences[:, 0] + differences[:, 1]))
        return cost

    def cost(self, path: Path) -> float:
        '''Return the Euclidean distance if the path is followed.'''
        return ccost.cost(self.cities, np.asarray(path))

    def _get_path_runs(self, path: Path, length: int) ->  List[int]:
        '''Generator for consecutive runs of a path'''
        runs = []
        for i in range(self.N):
            if i <= self.N - length:
                runs.append(path[i:(i + length)])
            else:
                # looping back around
                runs.append([*path[i:], *path[:(self.N - length + i)]])

        return runs

    def _two_opt_swap(self, path: Path, v1: int, v2: int):
        '''2-opt swap'''
        return [*path[:v1 + 1], *path[v2:v1:-1], *path[v2 + 1:]]

    def _find_neighbors_k_opt(self, path: Path, **kwargs) -> List[Path]:
        k = kwargs['k'] if 'k' in kwargs else 2

        if k != 2:
            raise NotImplementedError('Only 2-opt optimization supported.')
        
        neighbors = []
        
        for v1 in range(self.N):
            for v2 in range(v1 + 2, self.N):
                if self.N < 200 or ccost.shouldPerformTwoOptSwap(self.cities, np.asarray(path), v1, v2):
                    neighbors.append(self._two_opt_swap(path, v1, v2))
        
        return neighbors
        

    def find_neighbors(self, path: Path, method: str = 'opt', **kwargs) -> List[Path]:
        '''
        Find the neighbors of a solution.

        type corresponds to how we define a neighbor.
        - opt is related to k-opt optimization. For now, only 2-opt is implemented.
        '''
        if method == 'opt':
            return self._find_neighbors_k_opt(path, **kwargs)
        else:
            raise NotImplementedError('Only k-opt optimization supported.')

