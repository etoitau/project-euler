#The following iterative sequence is defined for the set 
# of positive integers:
# n → n/2 (n is even)
# n → 3n + 1 (n is odd)
# Using the rule above and starting with 13, we generate the 
# following sequence:
# 13 → 40 → 20 → 10 → 5 → 16 → 8 → 4 → 2 → 1
# It can be seen that this sequence (starting at 13 and finishing at 1) 
# contains 10 terms. Although it has not been proved yet 
# (Collatz Problem), it is thought that all starting numbers finish at 1.
# Which starting number, under one million, produces the longest chain?
# NOTE: Once the chain starts the terms are allowed to go above one million.
# Result: 837799

import math
from typing import Set, List, Tuple, Dict
from functools import reduce
import time
import sys
sys.path.append(".")
from util import prime_factors, triangle_number

def longest_collatz_under(n: int) -> Tuple[int, int]:
    memo: Dict[int, int] = dict()
    memo[1] = 1
    champ = 1
    result = 1
    for i in range(1, n):
        chain = collatz_depth(i, memo)
        if chain > result:
            result = chain
            champ = i
    return champ, result

def collatz_depth(n: int, memo: List[int]) -> int:
    if n in memo:
        return memo[n]
    elif n % 2:
        memo[n] = 1 + collatz_depth(3 * n + 1, memo)
    else:
        memo[n] = 1 + collatz_depth(n // 2, memo)
    return memo[n]

if __name__ == '__main__':
    """starts here"""
    n = 1000000
    start = time.time()
    print(longest_collatz_under(n)) # (837799, 525)
    print(time.time() - start) # 1.387 sec
