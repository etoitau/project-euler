# There are exactly ten ways of selecting three from five, 12345:
# 123, 124, 125, 134, 135, 145, 234, 235, 245, and 345
# In combinatorics we use the notation (5 | 3) = 10
# In general, (n | r) = n! / (r! * (n - r)!)
# It is not until n = 23, that a value exceeds one-million:
# (23 | 10) = 1144066 
# How many, not necessarily distinct, values of (n | r) for 1 <= n <= 100
# are greater than one-million?
# Result: 4075

from typing import Set, List, Tuple, Dict
import time
import sys
sys.path.append(".")
from util import Factorial, combination_count
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
    
if __name__ == '__main__':
    """starts here"""
    start = time.time()
    # for each n
    # check r = n / 2 to see if max is over limit
    # if not, skip
    # if so, binary search to find point where goes over
    # add 2 * (n / 2 - r) to count
    n_limit = 100
    count_limit = 1000000
    facts = Factorial()
    count = 0
    for n in range (n_limit + 1):
        if combination_count(n, n // 2, facts) <= count_limit:
            continue
        # binary search for where count goes over limit
        high = n // 2
        low = 1
        while high > low:
            mid = (high + low) // 2
            value = combination_count(n, mid, facts)
            if value > count_limit:
                high = mid
            elif value < count_limit:
                low = mid + 1
            else:
                low = mid
                high = mid
        count += n - low - low + 1
    print(count) # 4075
    print(time.time() - start) # 0.001 sec
