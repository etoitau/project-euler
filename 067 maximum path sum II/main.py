# By starting at the top of the triangle below and moving to 
# adjacent numbers on the row below, the maximum total from top to 
# bottom is 23.
# 3
# 7 4
# 2 4 6
# 8 5 9 3
# That is, 3 + 7 + 4 + 9 = 23.
# Find the maximum total from top to bottom in triangle.txt 
# (right click and 'Save Link/Target As...'), a 15K text file 
# containing a triangle with one-hundred rows.
# NOTE: This is a much more difficult version of Problem 18. 
# It is not possible to try every route to solve this problem, 
# as there are 299 altogether! If you could check one trillion 
# (1012) routes every second it would take over twenty billion 
# years to check them all. There is an efficient algorithm 
# to solve it. ;o)
# Result: 7273

import math
from typing import Generator, Set, List, Tuple, Dict
import time
import sys
sys.path.append(".")
from util import square_root_convergent_generator
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

def get_rows() -> List[List[int]]:
    rows: List[List[int]] = []
    with open(os.path.join(__location__, "p067_triangle.txt")) as f:
        for input in f:
            rows.append([ int(n) for n in input.split(" ") ])
    return rows

def max_path_sum(rows: List[List[int]]) -> int:
    """ Working from the bottom up, it's pretty trivial to determine
    the maximum path below a given node. 
    """
    for r in range(len(rows) - 2, -1, -1):
        for i in range(len(rows[r])):
            rows[r][i] += max(rows[r + 1][i], rows[r + 1][i + 1])
    return rows[0][0]

if __name__ == '__main__':
    """ starts here """
    test = [[3], [7, 4], [2, 4, 6], [8, 5, 9, 3]]
    start = time.time()
    print(max_path_sum(get_rows())) # 7273
    print(time.time() - start) # 0.006 sec
