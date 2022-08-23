# Traveling Salesman Problem with Tabu Search

Dawson Ren, July 15th, 2022

## The Traveling Salesman Problem
The travelling salesman problem is a classic problem in optimization. It involves finding the shortest possible route between a collection of cities. It is NP-hard, that is, the number of possible solutions grows combinatorially with the number of cities, making a brute force search impractical.

## Tabu Search
Instead of trying to find "the best route", we find one that is good enough. We can do this by exploiting local search, where we simply search the neighbors. However, this can cause us to become stuck in local minima. We avoid this by marking certain search options as "tabu", which we should never come back to. With this setup, we don't really see the benefits of Tabu Search until 50 cities, where the solution space is large and has more local minima.

## Additional Notes
We use Anaconda to manage packages for scientific computing. See the file `requirements.txt` to get started.

We use Cython to speed up computation and mypy to check types.

To run the Cython compilation, run the command `python3 pyx/setup.py build_ext --inplace`

To run the mypy type check, run the command `mypy .`. I didn't do a very good job adhering to their guidelines though...

With some simple benchmarking, I've found that the Cython compilation step reduces the solution time by 1.5x, which is non-negligible. However, the effort required to fully utilize Cython syntax is probably not worth the effort at this stage for further performance benefits. Instead, being conscious of vectorization and parallelism is probably the easier way to go, for example see the improved `cost()` method of the TSP class in `tsp.py`.

For this reason, the code in `/pyx` are not currently being developed.

To analyze the performance of the code, we use cProfile. To run the bash script that runs the profiling process, first make sure the scripts/profile.sh file is executable with `chmod +x scripts/profile.sh`, then run with `./scripts/profile.sh -r`. The resulting output will be in the `/profiles` folder. You can omit the `-r` flag if you want to keep the `.pstats` file generated from cProfile.

The `cost()` method is the source of most of the complexity. We implement the function using Cython for further performance benefits.


