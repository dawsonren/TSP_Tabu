#!/bin/bash

mkdir -p profiles
python3 -m cProfile -o output.pstats main.py
gprof2dot --colour-nodes-by-selftime -f pstats output.pstats | dot -Tpng -o profiles/output.png
rm output.pstats
