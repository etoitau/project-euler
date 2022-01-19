import math
from typing import Dict, Set, List
from functools import reduce

def gcd(a: int, b: int) -> int:
    """Greatest common denominator by Euler method"""
    while b:
        a, b = b, a % b
    return a 

def lcm(a: int, b: int) -> int:
    """Least common multiple"""
    return abs(a * b) // gcd(a, b)

def prime_sieve(n: int, primes: List[int]=[]) -> List[int]:
    """Get list of all primes less than or equal to n using Sieve of Eratosthenes
    Can optionally provide already calculated primes. 
    These should not be missing any in their range
    """
    sieve_start = 2
    is_prime = [True for i in range(n + 1)]
    if len(primes):
        sieve_start = primes[-1] + 1
        for i in range(primes[-1]):
            is_prime[i] = False
        for p in primes:
            is_prime[p] = True
            start = p ** 2
            if sieve_start > start:
                # Want to start at unknown #s, but need to start on mult of p
                start = sieve_start - (sieve_start % p)
            for i in range(start, n + 1, p):
                is_prime[i] = False
    c = sieve_start
    limit = math.sqrt(n)
    while (c <= limit):
        if (is_prime[c] == True):
            for i in range(c ** 2, n + 1, c):
                is_prime[i] = False
        c += 1
    is_prime[0]= False
    is_prime[1]= False
    for i in range(sieve_start, len(is_prime)):
        if is_prime[i]:
            primes.append(i)
    return primes

def nth_prime(n) -> int:
    """Return the nth prime number"""
    # Per prime number theorem, estimate upper bound
    upper_bound = 13 if n < 7 else round(n * (math.log(n) + math.log(math.log(n))) + 1)
    primes = prime_sieve(upper_bound)
    while len(primes) < n:
        # Look further if necessary (it shouldn't be)
        upper_bound = round(upper_bound * 1.5)
        primes = prime_sieve(upper_bound, primes)
    return primes[n - 1]


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

def triangle_number(nth: int) -> int:
    return nth * (nth + 1) // 2

if __name__ == '__main__':
    """starts here"""
    # print(nth_prime(6))
