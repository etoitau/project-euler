# It is possible to write five as a sum in exactly 
# six different ways:
# 4 + 1
# 3 + 2
# 3 + 1 + 1
# 2 + 2 + 1
# 2 + 1 + 1 + 1
# 1 + 1 + 1 + 1 + 1
# How many different ways can one hundred be written as a sum of 
# at least two positive integers?
# Result: 190569291

import math
from typing import Callable, Generator, Set, List, Tuple, Dict
import time
import sys
sys.path.append(".")
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

def solve(n: int) -> int:
    # Save seen results to avoid repeat work
    # -1 will mean not seen
    memo = [[ -1 for _ in range(n + 1) ] for _ in range(n + 1)]
    # Correct by 1 since the problem doesn't count n = n
    return count_sums(n, 1, memo) - 1

def count_sums(n: int, next: int, memo: List[List[int]]) -> int:
    if n == 0:
        return 1
    if n < next:
        return 0
    if memo[n][next] > -1:
        return memo[n][next]
    count = 0
    for to_sub in range(next, n + 1):
        count += count_sums(n - to_sub, to_sub, memo)
    memo[n][next] = count
    return count

if __name__ == '__main__':
    """ starts here """
    start = time.time()
    print(solve(100)) # 190,569,291
    print(time.time() - start) # 0.063 sec
