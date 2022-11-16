# The smallest number expressible as the sum of a prime square, 
# prime cube, and prime fourth power is 28. In fact, there are 
# exactly four numbers below fifty that can be expressed in such a way:
# 28 = 2^2 + 2^3 + 2^4
# 33 = 3^2 + 2^3 + 2^4
# 49 = 5^2 + 2^3 + 2^4
# 47 = 2^2 + 3^3 + 2^4
# How many numbers below fifty million can be expressed as the 
# sum of a prime square, prime cube, and prime fourth power?
# Result: 1097343

from typing import Callable, Generator, Set, List, Tuple, Dict
import time
import sys
import math

sys.path.append(".")
from util import prime_sieve
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))


def solve(limit: int) -> int:
    # The biggest prime we might need occurs when it is the 
    # squared power and the smallest prime is the cubed and fourth power term
    # sqrt(limit - 1 - 2^3 - 2^4)
    max_prime = math.ceil(math.sqrt(limit - 1 - 8 - 16))
    # Use the Sieve of Eratosthenes to get all primes up to that max prime
    primes = prime_sieve(max_prime)
    # Precompute and save the prime powers to avoid a lot of repeat work
    prime_powers: List[List[int]] = []
    for p in primes:
        powers = [1]
        for i in range(4):
            powers.append(p * powers[i])
        prime_powers.append(powers)
    # Add all the numbers we find to a set to discard duplicates
    expressible: Set[int] = set()
    for p1_index in range(len(prime_powers)):
        # Try each prime in the a^4 term, this will never be over limit
        p1_term = prime_powers[p1_index][4]
        for p2_index in range(len(prime_powers)):
            # Try each prime in the b^3 term.
            p2_term = p1_term + prime_powers[p2_index][3]
            # If this puts us over the limit, go to the next a value
            if p2_term > limit:
                break
            for p3_index in range(len(prime_powers)):
                # Try each prime in the c^2 term.
                p3_term = p2_term + prime_powers[p3_index][2]
                # If this puts us over the limit, go to the next b value
                if p3_term > limit:
                    break
                # This is a number under the limit made by p1^4 + p2^3 + p3^2
                expressible.add(p3_term)
    return len(expressible)

if __name__ == '__main__':
    """ starts here """
    start = time.time()
    # Examples: 50 -> 4
    print(solve(50000000)) # 1097343
    print(time.time() - start) # 0.381
