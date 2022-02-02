# Let d(n) be defined as the sum of proper divisors of n (numbers less than n which divide 
# evenly into n).
# If d(a) = b and d(b) = a, where a ≠ b, then a and b are an amicable pair and each of 
# a and b are called amicable numbers.
# For example, the proper divisors of 220 are 1, 2, 4, 5, 10, 11, 20, 22, 44, 55 and 110; 
# therefore d(220) = 284. The proper divisors of 284 are 1, 2, 4, 71 and 142; so d(284) = 220.
# Evaluate the sum of all the amicable numbers under 10000
# Result: 31626

import math
from typing import Set, List, Tuple, Dict
from functools import reduce
import time
import sys
sys.path.append(".")
from util import prime_sieve, prime_factors, factors_to_divisors


if __name__ == '__main__':
    """starts here"""
    n = 10000
    start = time.time()
    # pre-calc known primes in range
    known_primes = set(prime_sieve(n))
    # get divisors for each number
    #   get prime factorization
    #   multiply every combination of factors
    # sum divisors for each number to get d for each
    d_list = [ sum(factors_to_divisors(prime_factors(i, known_primes))) for i in range (n)]
    # scan for pairs and collect
    amicables = set()
    for a in range(2, len(d_list)):
        # amicable if d(a) = b and d(b) = a
        b = d_list[a]
        if b < n and d_list[b] == a and a != b:
            amicables.add(a)
    # return sum of collection
    print(sum(amicables)) # 31626
    print(time.time() - start) # 0.342 sec
