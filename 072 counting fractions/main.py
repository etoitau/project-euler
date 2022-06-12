# Consider the fraction, n/d, where n and d are positive 
# integers. If n<d and HCF(n,d)=1, it is called a reduced 
# proper fraction.
# If we list the set of reduced proper fractions for d ≤ 8 in 
# ascending order of size, we get:
# 1/8, 1/7, 1/6, 1/5, 1/4, 2/7, 1/3, 3/8, 2/5, 3/7, 1/2, 4/7, 
# 3/5, 5/8, 2/3, 5/7, 3/4, 4/5, 5/6, 6/7, 7/8
# It can be seen that there are 21 elements in this set.
# How many elements would be contained in the set of reduced 
# proper fractions for d ≤ 1,000,000?
# Result: 303963552391

import math
from typing import Callable, Generator, Set, List, Tuple, Dict
import time
import sys
sys.path.append(".")
from util import Frac
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

def solve(limit: int) -> int:
    # Build an array where the value at each index is how many
    # new fractions the a denominator with the value of that index
    # adds to the count compared with all before
    # e.g. 2 adds one, 1/2, so any multiple of two should have 1 
    # subtracted from it's count.
    # Note I'm counting 1/1 as a fraction to make this work, 
    # then removing it at the end.
    counts = [ n for n in range(limit + 1) ]
    for n in range(1, limit + 1):
        curr = n + n
        count = counts[n]
        while curr <= limit:
            counts[curr] -= count
            curr += n
    return sum(counts) - 1

if __name__ == '__main__':
    """ starts here """
    start = time.time()
    limit = 1000000
    print(solve(limit)) # 303963552391
    print(time.time() - start) # 3.861 sec
