'''
Provide the LocalSearch and TabuSearch classes.
'''
from typing import Optional
from shared.interfaces import SearchProtocol, Problem, Solution, Path
from tsp_solution import TSPSolution

class LocalSearch(SearchProtocol):
    def __init__(self) -> None:
        self.max_iter = 50
        self.iters = 0

    def stoppingCondition(self) -> bool:
        return self.iters > self.max_iter

    def search(self, problem: Problem, starting_solution: Solution, verbose = True) -> Solution:
        best_path = starting_solution.path()
        best_candidate = starting_solution.path()
        best_candidate_cost = None
        while not self.stoppingCondition():
            self.iters += 1
            neighborhood = problem.find_neighbors(best_path)
            best_candidate = neighborhood[0]
            best_candidate_cost = problem.cost(best_candidate)

            for candidate in neighborhood:
                if problem.cost(candidate) < best_candidate_cost:
                    best_candidate = candidate
                    best_candidate_cost = problem.cost(best_candidate)
            
            if best_candidate_cost < problem.cost(best_path):
                best_path = best_candidate
                if verbose:
                    print(f'Solution was improved! {best_path}')
            else:
                if verbose:
                    print('Stuck in a local minima...')
                break
        
        starting_solution.set_path(best_path)
        return starting_solution


class TabuSearch(SearchProtocol):
    def __init__(self) -> None:
        super().__init__()
        self.max_iter = 100
        self.iters = 0
        self.max_tabu_size = 100

    def stoppingCondition(self) -> bool:
        return self.iters > self.max_iter

    def _pop_first(self, d: dict) -> dict:
        '''Pop the first element from a dictionary. Could use OrderedDict, but found this in CPython 3 Docs.'''
        k = next(iter(d))
        d.pop(k)
        return d

    def search(self, problem: Problem, starting_solution: Solution, verbose = True) -> Solution:
        best_path = starting_solution.path()
        best_inter = starting_solution.path() # intermediate, not the best path but better than the candidate
        # use tuples as immutable type to check membership
        # use dictionary to support O(1) insertion/membership check
        tabu_list = dict[Path, bool]([(tuple(starting_solution.path()), True)])

        while not self.stoppingCondition():
            self.iters += 1
            neighborhood = problem.find_neighbors(best_inter)
            best_candidate: Optional[Path] = None

            # find the best candidate that's not in the tabu list
            for candidate in neighborhood:
                if best_candidate is None:
                    if not tuple(candidate) in tabu_list:
                        best_candidate = candidate
                    else:
                        continue

                if problem.cost(candidate) < problem.cost(best_candidate) and not tuple(candidate) in tabu_list:
                    best_candidate = candidate

            if best_candidate is None:
                if verbose:
                    print('There are no neighbors that can be selected because they are all in the tabu list.')
                break
            
            # set intermediate to best candidate
            best_inter = best_candidate
            if problem.cost(best_candidate) < problem.cost(best_path):
                if verbose:
                    print(f'Solution was improved!\n{best_path}')
                # set best path to our newly found one
                best_path = best_inter
            else:
                if verbose:
                    print(f'Solution was not able to be improved, but taking the next best option...\n{best_inter}')
            
            # make sure we don't revisit this best candidate
            tabu_list[tuple(best_candidate)] = True

            # make sure tabu_list doesn't get too large for performance reasons
            if len(tabu_list) > self.max_tabu_size:
                tabu_list = self._pop_first(tabu_list)

        starting_solution.set_path(best_path)
        return starting_solution
