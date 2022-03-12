# The prime 41, can be written as the sum of six consecutive primes:
# 41 = 2 + 3 + 5 + 7 + 11 + 13
# This is the longest sum of consecutive primes that adds to 
# a prime below one-hundred.
# The longest sum of consecutive primes below one-thousand 
# that adds to a prime, contains 21 terms, and is equal to 953.
# Which prime, below one-million, can be written as the sum of 
# the most consecutive primes?
# Result: 997651

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
    # we already know of 21 terms that sum to 953
    # sum not > 1000000
    limit = 1000000
    # Precalculate primes using sieve
    pm = PrimeMachine(limit)
    best = 21
    best_sum = 953
    for first in range(78476): # 78497 is index of last prime under a mil
        last = first + 1
        curr_sum = pm.get(first) + pm.get(last)
        while curr_sum < limit:
            if pm.is_prime(curr_sum):
                if 1 + last - first > best:
                    best = 1 + last - first
                    best_sum = curr_sum
            last += 1
            curr_sum += pm.get(last)
    print(best_sum) # 997651
    print(time.time() - start) # 0.811 sec
