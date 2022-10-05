#!/bin/bash

# -r : remove output.pstats after finishing

RFLAG="1"

while getopts 'r' OPTION; do
    case "$OPTION" in
        r)
            RFLAG=""
            ;;
        ?)
            echo "script usage: $(basename \$0) [-r]" >&2
            exit 1
            ;;
    esac
done

mkdir -p profiles
python3 -m cProfile -o output.pstats main.py
gprof2dot --colour-nodes-by-selftime -f pstats output.pstats | dot -Tpng -o profiles/output.png
if [ -z $RFLAG ]; then
    rm output.pstats
fi
