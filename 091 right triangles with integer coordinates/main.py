# The points P (x1, y1) and Q (x2, y2) are plotted at integer 
# co-ordinates and are joined to the origin, O(0,0), to form ΔOPQ.
# There are exactly fourteen triangles containing a right angle 
# that can be formed when each co-ordinate lies between 0 and 2 
# inclusive; that is,
# 0 ≤ x1, y1, x2, y2 ≤ 2.
# Given that 0 ≤ x1, y1, x2, y2 ≤ 50, how many right triangles 
# can be formed?
# Result: 14234

from typing import Callable, Generator, Set, List, Tuple, Dict
import time
import sys
import math
from collections import OrderedDict

sys.path.append(".")
from util import combinations_no_repeats
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))


def point_to_index(x: int, y: int, dim: int) -> int:
    return y * (dim + 1) + x

def index_to_point(i: int, dim: int) -> Tuple[int, int]:
    return (i % (dim + 1), i // (dim + 1))

def square_list(through: int) -> List[int]:
    return [ i * i for i in range(through + 1) ]

def solve(dim: int) -> int:
    count = 0
    # as a simple way to consider each pair of points in the grid,
    # consider indexing each grid point and iterating over that index 
    max_i = point_to_index(dim, dim, dim)
    # we will need the square of each dimension many times, cache them
    squares = square_list(dim)
    for i in range(1, max_i):
        # the point represented by index i
        xi, yi = index_to_point(i, dim)
        # dx^2 + dy^2 for the line O -> i
        oix2y2 = squares[xi] + squares[yi]
        for j in range(i + 1, max_i + 1):
            # the point represented by index j
            xj, yj = index_to_point(j, dim)
            # dx^2 + dy^2 for the line o -> j
            ojx2y2 = squares[xj] + squares[yj]
            # dx^2 + dy^2 for the line i -> j
            ijx2y2 = squares[abs(xj - xi)] + squares[abs(yj - yi)]
            # we could figure out which is largest, but it's probably
            # as fast to just check each 
            if oix2y2 == ojx2y2 + ijx2y2 \
                or ojx2y2 == oix2y2 + ijx2y2 \
                    or ijx2y2 == oix2y2 + ojx2y2:
                    count += 1
    return count

if __name__ == '__main__':
    """ starts here """
    
    start = time.time()
    # print(point_to_index(2, 2, 2))
    print(solve(50)) # 14234
    print(time.time() - start) # 1.912
