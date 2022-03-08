# We shall say that an n-digit number is pandigital if it makes use of all the 
# digits 1 to n exactly once. For example, 2143 is a 4-digit pandigital and 
# is also prime.
# What is the largest n-digit pandigital prime that exists?
# Result: 7652413

import math
from typing import Set, List, Tuple, Dict
from functools import reduce
import time
import sys
sys.path.append(".")
from util import is_pandigital, prime_sieve
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

    
if __name__ == '__main__':
    """starts here"""
    start = time.time()
    # Can't be 9 or 8 digit number bc sum of digits would 
    # always be 45 and 36 respectively if they're pandigital.
    # Both are divisible by 3 so we know they aren't prime 
    primes = prime_sieve(7654321)
    for p in reversed(primes):
        if is_pandigital(p):
            print(p) # 7652413
            break
    print(time.time() - start) # 1.784 sec
