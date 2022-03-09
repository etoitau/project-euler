# The first two consecutive numbers to have two distinct 
# prime factors are:
# 14 = 2 × 7
# 15 = 3 × 5
# The first three consecutive numbers to have three distinct 
# prime factors are:
# 644 = 2² × 7 × 23
# 645 = 3 × 5 × 43
# 646 = 2 × 17 × 19.
# Find the first four consecutive integers to have four 
# distinct prime factors each. What is the first of these numbers?
# Result: 134043

from itertools import permutations
import math
from typing import Set, List, Tuple, Dict
from functools import reduce
import time
import sys
sys.path.append(".")
from util import PrimeMachine
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
    
if __name__ == '__main__':
    """starts here"""
    start = time.time()
    pm = PrimeMachine()
    first = 1
    series = 4
    while True:
        end = first
        while (end - first) < series and len(pm.prime_factors(end)) >= series:
            end += 1
        if end - first >= series:
            print(first) # 134043
            break
        first = end + 1
    print(time.time() - start) # 3.002 sec
