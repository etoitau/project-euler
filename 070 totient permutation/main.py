# Euler's Totient function, φ(n) [sometimes called the phi 
# function], is used to determine the number of positive 
# numbers less than or equal to n which are relatively prime 
# to n. For example, as 1, 2, 4, 5, 7, and 8, are all less 
# than nine and relatively prime to nine, φ(9)=6.
# The number 1 is considered to be relatively prime to every 
# positive number, so φ(1)=1.
# Interestingly, φ(87109)=79180, and it can be seen that 
# 87109 is a permutation of 79180.
# Find the value of n, 1 < n < 107, for which φ(n) is a 
# permutation of n and the ratio n/φ(n) produces a minimum.
# Result: 8319823

import math
from typing import Generator, Set, List, Tuple, Dict
import time
import sys
sys.path.append(".")
from util import PrimeMachine, int_to_int_array, is_permutation, totient
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

def solve_thorough(to: int) -> int:
    # too slow, but makes no assumptions, checks every possibility
    pm = PrimeMachine(math.ceil(math.sqrt(to)))
    min_ratio = to
    result = 0
    for n in range(2, to):
        tot = totient(n, pm)
        if is_permutation(int_to_int_array(tot), int_to_int_array(n)):
            ratio = n / tot
            if ratio < min_ratio:
                min_ratio = ratio
                result = n
    return result

def solve(to: int) -> int:
    # From Euler's product formula we can see that generally
    # n / phi will be smaller with fewer prime factors.
    # Try looking for a solution with only two prime factors.
    # And larger primes will also lead to smaller n / phi, so
    # look for a solution which uses large primes with no power.
    pm = PrimeMachine()
    min_ratio = to
    result = 0
    i = 0
    j = 0
    pi = pm.get(i)
    pi_limit = math.floor(math.sqrt(to))
    while True:
        # get the next second prime
        j += 1
        pj = pm.get(j)
        n = pi * pj
        if n > to:
            # over the prescribed limit, start over with the next
            # first prime, unless it's too large, in which case
            # we're done.
            i += 1
            j = i
            pi = pm.get(i)
            if pi > pi_limit:
                break
            continue
        # simplification of euler's product formula
        # for just two primes
        tot = (pi - 1) * (pj - 1)
        if is_permutation(int_to_int_array(tot), int_to_int_array(n)):
            ratio = n / tot
            if ratio < min_ratio:
                min_ratio = ratio
                result = n
    return result

if __name__ == '__main__':
    """ starts here """
    start = time.time()
    limit = 10000000
    print(solve(limit)) # 8319823 
    print(time.time() - start) # 19.408 sec
