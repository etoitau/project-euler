# Euler discovered the remarkable quadratic formula:
# n^2 + n + 41
# It turns out that the formula will produce 40 primes for the 
# consecutive integer values . However, when  is divisible by 41, 
# and certainly when  is clearly divisible by 41.
# The incredible formula n^2 - 79n + 1601 was discovered, 
# which produces 80 primes for the consecutive values 0 <= n <= 79. 
# The product of the coefficients, −79 and 1601, is −126479.
# Considering quadratics of the form:
# n^2 + an + b where |a| < 1000 and |b| <= 1000
# where |n| is the modulus/absolute value of n
# e.g. |11| = 11 and |-4| = 4 
# Find the product of the coefficients, a and b, for the 
# quadratic expression that produces the maximum number of primes 
# for consecutive values of n, starting with n = 0.
# Result: -59231

import math
from typing import Set, List, Tuple, Dict
from functools import reduce
import time
import sys
sys.path.append(".")
from util import PrimeMachine, fibonacci_generator
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

if __name__ == '__main__':
    """starts here"""
    # result for n = 0 can't be < 1, so a > -(b + 1)
    # result must be prime for n = 0, so b must be prime
    # will need to itt over primes for b values and have a 
    # set of primes for fast checking. Don't know max limit 
    # in advance.
    start = time.time()
    max_run = 40
    max_a = 1
    max_b = 41
    prime_machine = PrimeMachine()
    for b in prime_machine:
        if b > 1000:
            break
        for a in range(-1 * b, 1000):
            n = 0
            while prime_machine.is_prime(n**2 + a * n + b):
                n += 1
            if n > max_run:
                max_run = n
                max_a = a
                max_b = b
    print(max_a * max_b) # -59231
    print(time.time() - start) # 0.3458 sec
