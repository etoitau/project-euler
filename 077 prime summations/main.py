# It is possible to write ten as the sum of primes in exactly five 
# different ways:
# 7 + 3
# 5 + 5
# 5 + 3 + 2
# 3 + 3 + 2 + 2
# 2 + 2 + 2 + 2 + 2
# What is the first value which can be written as the sum of primes in 
# over five thousand different ways?
# Result: 71

import math
from typing import Callable, Generator, Set, List, Tuple, Dict
import time
import sys
sys.path.append(".")
from util import PrimeMachine
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

def solve(ways: int) -> int:
    # Save seen results to avoid repeat work
    memo: Dict[Tuple[int, int], int] = dict()
    pm = PrimeMachine()
    n = 9
    count = 0
    while count <= ways:
        n += 1
        # Correct by 1 since the problem doesn't count n = n
        # but this will only occur if n is prime
        count = count_sums(n, 0, memo, pm) - (1 if pm.is_prime(n) else 0) 
    return n

def count_sums(n: int, nth_prime: int, memo: Dict[Tuple[int, int], int], pm: PrimeMachine) -> int:
    if n == 0:
        return 1
    next = pm.get(nth_prime)
    if n < next:
        return 0
    key = (n, nth_prime)
    if key in memo:
        return memo[key]
    count = 0
    prime_index = nth_prime
    while next <= n:
        count += count_sums(n - next, prime_index, memo, pm)
        prime_index += 1
        next = pm.get(prime_index)
    memo[key] = count
    return count

if __name__ == '__main__':
    """ starts here """
    start = time.time()
    print(solve(5000)) # 71
    print(time.time() - start) # 0.005 sec
