import numpy as np

cimport numpy as np

np.import_array()

INT = np.int
FLOAT = np.float

ctypedef np.int_t INT_t
ctypedef np.float_t FLOAT_t

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
