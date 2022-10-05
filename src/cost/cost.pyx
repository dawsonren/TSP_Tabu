import numpy as np

cimport numpy as np
cimport cython

np.import_array()

INT = np.int
FLOAT = np.float

ctypedef np.int_t INT_t
ctypedef np.float_t FLOAT_t

@cython.boundscheck(False) # turn off bounds-checking for entire function
@cython.wraparound(False) # turn off negative indexing for entire function
def cost(np.ndarray[FLOAT_t, ndim=2] cities, np.ndarray[INT_t, ndim=1] path):
    if cities.shape[1] != 2:
        raise ValueError('Argument cities must have exactly two columns.')
    if cities.shape[0] != path.shape[0]:
        raise ValueError('Path and cities have unresolvable lengths.')

    assert cities.dtype == FLOAT and path.dtype == INT

    cdef np.ndarray shifted_cities = np.vstack((cities[path[1:], :], cities[path[0], :]))
    cdef np.ndarray differences = np.power(cities[path] - shifted_cities, 2)
    cdef float cost = np.sum(np.sqrt(differences[:, 0] + differences[:, 1]))

    return cost

# Used to more efficiently compare partial paths
# Doesn't take the square room of the distance and doesn't complete the path (acyclic)
@cython.boundscheck(False)
def relative_cost(np.ndarray[FLOAT_t, ndim=2] cities, np.ndarray[INT_t, ndim=1] path):
    if cities.shape[1] != 2:
        raise ValueError('Argument cities must have exactly two columns.')

    assert cities.dtype == FLOAT and path.dtype == INT

    cdef np.ndarray differences = np.power(cities[path[:-1]] - cities[path[1:]], 2)
    cdef float cost = np.sum(differences)

    return cost

# Check whether or not we should perform a 2-opt swap in O(1) time
@cython.wraparound(False) # turn off negative indexing for entire function
def shouldPerformTwoOptSwap(np.ndarray[FLOAT_t, ndim=2] cities, np.ndarray[INT_t, ndim=1] path, int v1, int v2):
    cdef int n = path.shape[0]
    cdef float old_path1 = np.sum(np.power(cities[path[v1], :] - cities[path[(v1 + 1) % n], :], 2))
    cdef float old_path2 = np.sum(np.power(cities[path[v2], :] - cities[path[(v2 + 1) % n], :], 2))
    cdef float new_path1 = np.sum(np.power(cities[path[(v1 + 1) % n], :] - cities[path[(v2 + 1) % n], :], 2))
    cdef float new_path2 = np.sum(np.power(cities[path[v1], :] - cities[path[v2], :], 2))

    cdef float lengthDelta = new_path1 + new_path2 - old_path1 - old_path2

    return lengthDelta < 0