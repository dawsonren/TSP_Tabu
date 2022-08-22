from shared.interfaces import Path, Solution
 
class TSPSolution(Solution):
    def __init__(self, N) -> None:
        self.N = N
        self._path = list(range(N))

    def path(self):
        return self._path.copy()

    def set_path(self, path: Path):
        if sorted(path) != list(range(self.N)):
            raise ValueError('Path set violated invariant - all cities must be included only once')
        self._path = path

    def _reformat_path(self, path: Path) -> Path:
        '''Reformat path so that 0 is the first entry'''
        i = path.index(0)
        return [*path[i:], *path[:i]]
