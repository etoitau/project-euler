# Consider the fraction, n/d, where n and d are positive 
# integers. If n<d and HCF(n,d)=1, it is called a reduced 
# proper fraction.
# If we list the set of reduced proper fractions for d ≤ 8 
# in ascending order of size, we get:
# 1/8, 1/7, 1/6, 1/5, 1/4, 2/7, 1/3, 3/8, 2/5, 3/7, 1/2, 
# 4/7, 3/5, 5/8, 2/3, 5/7, 3/4, 4/5, 5/6, 6/7, 7/8
# It can be seen that there are 3 fractions between 1/3 and 1/2.
# How many fractions lie between 1/3 and 1/2 in the sorted 
# set of reduced proper fractions for d ≤ 12,000?
# Result: 7295372

import math
from typing import Callable, Generator, Set, List, Tuple, Dict
import time
import sys
sys.path.append(".")
from util import Frac
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

def solve(min: float, max: float, max_denom: int) -> int:
    # count how many fractions exist in the range for each denominator
    # where the denominator is the index into counts
    counts = [0] * (max_denom + 1)
    for d in range(2, max_denom + 1):
        min_num = math.ceil(min * d)
        min_val = min_num / d
        if min == min_val:
            min_num += 1
            min_val = min_num / d
        if not min < min_val < max:
            continue
        max_num = math.floor(max * d)
        max_val = max_num / d
        if max == max_val:
            max_num -= 1
            max_val = max_num / d
        counts[d] = max_num - min_num + 1
    # Note every fraction in one denom will also be currently counted 
    # in each multiple of that denom. Weed out the repeats 
    for n in range(1, max_denom + 1):
        curr = n + n
        count = counts[n]
        if not count:
            continue
        while curr <= max_denom:
            counts[curr] -= count
            curr += n
    return sum(counts)

if __name__ == '__main__':
    """ starts here """
    start = time.time()
    limit = 12000
    print(solve(1/3, 1/2, limit)) # 7295372
    print(time.time() - start) # 0.026 sec
