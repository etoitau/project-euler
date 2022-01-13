# By listing the first six prime numbers: 2, 3, 5, 7, 11, and 13, 
# we can see that the 6th prime is 13.
# What is the 10 001st prime number?
# Result: 104743

import math
from typing import Set
from functools import reduce
import time
import sys
sys.path.append(".")
from util import nth_prime

def nth_prime_naive(n) -> int:
    # while len primes < n
    # check next number, if any existing primes div w 0 mod, skip
    # start with 2, only check odds
    primes = [2]
    c = 3
    while len(primes) < n:
        is_prime = True
        for p in primes:
            if not c % p:
                is_prime = False
                break
        if is_prime:
            primes.append(c)
        c += 2
    return primes[-1]


if __name__ == '__main__':
    """starts here"""
    n = 10001
    start = time.time()
    print(nth_prime_naive(n))
    print(time.time() - start) # 2.534 sec
    start = time.time()
    print(nth_prime(n))
    print(time.time() - start) # 0.029 sec
