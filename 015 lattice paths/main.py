# Starting in the top left corner of a 2×2 grid, and only being 
# able to move to the right and down, there are exactly 6 routes 
# to the bottom right corner.
# How many such routes are there through a 20×20 grid?
# Result: 137846528820

import math
from typing import Set, List, Tuple, Dict
from functools import reduce
import time
import sys
sys.path.append(".")
from util import prime_factors, triangle_number

def lattice_routes(n: int) -> int:
    # We're basically filling in the number of ways to get to each point
    # starting at the top row and working our way down to the bottom
    # But since a cell's new value only depends on its previous value and 
    # the value to the left, we don't actually need to keep a 2d array
    # and can just update a vector n times.

    # +1 because one more lattice than grid space
    row =  [1 for i in range(n + 1) ]
    for i in range(n):
        # for each row in lattice
        for j in range(1, len(row)):
            # for each point in row, could get here from above 
            # or to the left, so add those
            row[j] += row[j - 1]
    return row[-1]

if __name__ == '__main__':
    """starts here"""
    n = 20
    start = time.time()
    print(lattice_routes(n)) # 137846528820
    print(time.time() - start) # 0.0 sec
