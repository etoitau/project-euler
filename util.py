import math
from typing import Dict, Set
from functools import reduce

def gcd(a: int, b: int) -> int:
    """Greatest common denominator by Euler method"""
    while b:
        a, b = b, a % b
    return a 

def lcm(a: int, b: int) -> int:
    """Least common multiple"""
    return abs(a * b) // gcd(a, b)

def prime_factors(n: int) -> Dict[int, int]:
    """Get the prime factorization of the input. The result takes the form 
    of a dict where the keys are the primes and the values are how many times
    that prime occurs in the factorization.
    """
    factors = dict([(1, 1)])
    primes_helper(n, factors)
    return factors

def primes_helper(n, factors: Dict[int, int]) -> None:
    """Recursive helper to do factorization by the tree method"""
    if n in factors:
        factors[n] += 1
        return
    d = math.floor(math.sqrt(n))
    while d > 1:
        if not n % d:
            primes_helper(d, factors)
            primes_helper(int(n / d), factors)
            return
        d -= 1
    factors[n] = 1

def recombine(factors: Dict[int, int]) -> int:
    """Take a factorization of the form produced by prime_factors and put
    back together into the original number.
    """
    result = 1
    for f in factors:
        result *= int(math.pow(f, factors[f]))
    return result

if __name__ == '__main__':
    """starts here"""
    print(recombine(prime_factors(100)))
