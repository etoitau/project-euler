# 2520 is the smallest number that can be divided by each of the numbers 
# from 1 to 10 without any remainder.
# What is the smallest positive number that is evenly divisible by all of the 
# numbers from 1 to 20?
# Result: 232792560

import math
from typing import Set
from functools import reduce
import time
import sys
sys.path.append(".")
from util import prime_factors, recombine

def smallest_mult_primes() -> int:
    """Much more efficient solution using prime factorization method"""
    factors = dict([(1,1)])
    for n in range(20, 1, -1):
        n_factors = prime_factors(n)
        for f in n_factors:
            if f not in factors or (f in factors and n_factors[f] > factors[f]):
                factors[f] = n_factors[f]
    return recombine(factors)

def smallest_mult() -> int:
    """Naive solution"""
    # Note checking 1-10 would be redundant (e.g if 18 divides evenly so will 9)
    to_check = [19, 18, 17, 16, 15, 14, 13, 12, 11]
    # A known common multiple, but hopefully not the smallest
    limit = reduce(lambda a, b: a * b, to_check) * 20
    n = 0
    while n < limit:
        n += 20
        is_mult = True
        for m in to_check:
            if n % m:
                is_mult = False
                break
        if is_mult:
            return n 
    return n


if __name__ == '__main__':
    """starts here"""
    start = time.time()
    print(smallest_mult())
    print(time.time() - start) # 2.12501
    start = time.time()
    print(smallest_mult_primes())
    print(time.time() - start) # 0.00012
