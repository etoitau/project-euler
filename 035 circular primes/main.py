# The number, 197, is called a circular prime because all 
# rotations of the digits: 197, 971, and 719, are themselves 
# prime.
# There are thirteen such primes below 100: 
# 2, 3, 5, 7, 11, 13, 17, 31, 37, 71, 73, 79, and 97.
# How many circular primes are there below one million?
# Result: 55

import math
from typing import Set, List, Tuple, Dict
from functools import reduce
import time
import sys
sys.path.append(".")
from util import PrimeMachine, int_array_to_int, int_to_int_array, rotations
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

def count_circular(limit: int):
    pm = PrimeMachine(limit)
    count = 0
    for p in pm:
        # for each prime less than the limit
        if p >= limit:
            break
        as_array = int_to_int_array(p)
        is_circular = True
        for rot in rotations(as_array):
            # check each rotation is also prime
            if not pm.is_prime(int_array_to_int(rot)):
                is_circular = False
                break
        if is_circular:
            # if so, count
            count += 1
    return count

if __name__ == '__main__':
    """starts here"""
    start = time.time()
    n = 1000000
    print(count_circular(n)) # 55
    print(time.time() - start) # 1.457 sec
