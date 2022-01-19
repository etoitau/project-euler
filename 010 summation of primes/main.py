# The sum of the primes below 10 is 2 + 3 + 5 + 7 = 17.
# Find the sum of all the primes below two million.
# Result: 142913828922

import math
from typing import Set, List, Tuple
from functools import reduce
import time
import sys
sys.path.append(".")
from util import prime_sieve

def sum_primes_below(n: int) -> int:
    return reduce(lambda a, b: a + b, prime_sieve(n - 1))

if __name__ == '__main__':
    """starts here"""
    n = 2000000
    start = time.time()
    print(sum_primes_below(n))
    print(time.time() - start) # 0.431 sec
