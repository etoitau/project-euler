# Euler's Totient function, φ(n) [sometimes called the phi 
# function], is used to determine the number of numbers less 
# than n which are relatively prime to n. For example, 
# as 1, 2, 4, 5, 7, and 8, are all less than nine and relatively 
# prime to nine, φ(9)=6.
# n	Relatively Prime	φ(n)	n/φ(n)
# 2	    1	            1	    2
# 3	    1,2	            2	    1.5
# 4	    1,3	            2	    2
# 5	    1,2,3,4	        4       1.25
# 6	    1,5	            2   	3
# 7	    1,2,3,4,5,6	    6   	1.1666...
# 8	    1,3,5,7	        4   	2
# 9	    1,2,4,5,7,8	    6   	1.5
# 10	1,3,7,9	        4   	2.5
# It can be seen that n=6 produces a maximum n/φ(n) for n ≤ 10.
# Find the value of n ≤ 1,000,000 for which n/φ(n) is a maximum
# Result: 510510

import math
from typing import Generator, Set, List, Tuple, Dict
import time
import sys
sys.path.append(".")
from util import PrimeMachine, gcd
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

def solve_naive(to: int) -> int:
    # Works, but too slow
    max_n = 2
    max_n_over_phi = 2
    for n in range(2, to + 1, 2):
        phi_limit = n / max_n_over_phi
        count = 0
        for r in range(1, n, 2):
            if gcd(n, r) == 1:
                count += 1
                if count > phi_limit:
                    break
        new_ratio = n / count
        if new_ratio > max_n_over_phi:
            max_n_over_phi = new_ratio
            max_n = n
    return max_n

def solve(to: int) -> int:
    # Credit to https://www.mathblog.dk/
    pm = PrimeMachine(20)
    result = 1
    for p in pm:
        result *= p
        if result > to:
            return result // p

if __name__ == '__main__':
    """ starts here """
    start = time.time()
    print(solve(1000000)) # 510510
    print(time.time() - start) # 0.001 sec
