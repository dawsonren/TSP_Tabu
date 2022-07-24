# Traveling Salesman Problem with Tabu Search

Dawson Ren, July 15th, 2022

## The Traveling Salesman Problem
The travelling salesman problem is a classic problem in optimization. It involves finding the shortest possible route between a collection of cities. It is NP-hard, that is, the number of possible solutions grows combinatorially with the number of cities, making a brute force search impractical.

## Tabu Search
Instead of trying to find "the best route", we find one that is good enough. We can do this by exploiting local search, where we simply search the neighbors. However, this can cause us to become stuck in local minima. We avoid this by marking certain search options as "tabu", which we should never come back to.

## Additional Notes
We use Cython to speed up computation and mypy to check types.

To run the Cython compilation, run the command `python3 cython/setup.py build_ext --inplace`.