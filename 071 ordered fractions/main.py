# Consider the fraction, n/d, where n and d are positive 
# integers. If n<d and HCF(n,d)=1, it is called a reduced 
# proper fraction.
# If we list the set of reduced proper fractions for d ≤ 8 
# in ascending order of size, we get:
# 1/8, 1/7, 1/6, 1/5, 1/4, 2/7, 1/3, 3/8, 2/5, 3/7, 1/2, 
# 4/7, 3/5, 5/8, 2/3, 5/7, 3/4, 4/5, 5/6, 6/7, 7/8
# It can be seen that 2/5 is the fraction immediately to 
# the left of 3/7.
# By listing the set of reduced proper fractions for 
# d ≤ 1,000,000 in ascending order of size, find the 
# numerator of the fraction immediately to the left of 3/7.
# Result: 428570

import math
from typing import Callable, Generator, Set, List, Tuple, Dict
import time
import sys
sys.path.append(".")
from util import Frac
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

def solve(d_max: int) -> int:
    target = 3/7
    best = Frac(2, 5)
    best_diff = target - best.get_float()
    for denom in range(d_max // 2, d_max + 1):
        # Don't need to check smaller d because they 
        # will be covered by the d twice as large
        if not denom % 7:
            # avoid exact matches
            continue
        num = 3 * denom // 7
        guess = Frac(num, denom)
        diff = target - guess.get_float()
        if diff < best_diff:
            best = guess
            best_diff = diff
    return best.simplify().n

if __name__ == '__main__':
    """ starts here """
    start = time.time()
    limit = 1000000
    print(solve(limit)) # 428570
    print(time.time() - start) # 0.330 sec
