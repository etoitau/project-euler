# The number 3797 has an interesting property. Being prime 
# itself, it is possible to continuously remove digits from 
# left to right, and remain prime at each stage: 3797, 797, 97, 
# and 7. Similarly we can work from right to left: 3797, 379, 37, 
# and 3.
# Find the sum of the only eleven primes that are both 
# truncatable from left to right and right to left.
# NOTE: 2, 3, 5, and 7 are not considered to be truncatable primes.
# Result: 748317

import math
from typing import Set, List, Tuple, Dict
from functools import reduce
import time
import sys
sys.path.append(".")
from util import PrimeMachine, get_palindromes, int_array_to_int, int_to_int_array, is_palindrome, rotations, to_array_base
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))


if __name__ == '__main__':
    """starts here"""
    start = time.time()
    # these don't count in themselves, but it's ok if we get
    # there by truncating
    dont_count = [ 2, 3, 5, 7 ]
    # Keep sets of known truncatable primes, we'll build these
    # up in a dynamic programming way.
    # These stay prime as you truncate from the left
    left_trunc = set(dont_count)
    # These stay prime if you truncate from the right
    right_trunc = set(dont_count)
    # These stay prime if you truncate from the right or left
    trunc_primes = set()
    pm = PrimeMachine()
    for p in pm:
        if p < 10:
            continue
        as_array = int_to_int_array(p)
        truncatable = True
        left = int_array_to_int(as_array[1:])
        if left in left_trunc:
            left_trunc.add(p)
        else:
            truncatable = False
        right = int_array_to_int(as_array[:-1])
        if right in right_trunc:
            right_trunc.add(p)
        else:
            truncatable = False
        if truncatable:
            print(p)
            trunc_primes.add(p)
            if len(trunc_primes) == 11:
                break
    print(sum(trunc_primes)) # 748317
    print(time.time() - start) # 0.841 sec
