# The prime factors of 13195 are 5, 7, 13 and 29.
# What is the largest prime factor of the number 600851475143 ?
# Result: 6857

import math
from typing import Set

def max_factor(n):
    return max(prime_factors(n))

def prime_factors(n) -> Set:
    primes = set([1])
    non_primes: Set[int] = set()
    primes_helper(n, primes, non_primes)
    return primes

def primes_helper(n, primes: Set, non_primes: Set):
    if n in primes or n in non_primes:
        return
    d = math.floor(math.sqrt(n))
    while d > 1:
        if d not in primes and d not in non_primes and not n % d:
            non_primes.add(n)
            primes_helper(d, primes, non_primes)
            primes_helper(int(n / d), primes, non_primes)
            return
        d -= 1
    primes.add(n)

if __name__ == '__main__':
    """starts here"""
    print(max_factor(600851475143))