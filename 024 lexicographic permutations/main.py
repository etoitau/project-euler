# A permutation is an ordered arrangement of objects. For example, 3124 is one 
# possible permutation of the digits 1, 2, 3 and 4. If all of the permutations are 
# listed numerically or alphabetically, we call it lexicographic order. The 
# lexicographic permutations of 0, 1 and 2 are:
# 012   021   102   120   201   210
# What is the millionth lexicographic permutation of the 
# digits 0, 1, 2, 3, 4, 5, 6, 7, 8 and 9?
# Result: 

import math
from typing import Set, List, Tuple, Dict
from functools import reduce
import time
import sys
sys.path.append(".")
from util import lexilogical_permutation_generator, lexographic_permutation
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

if __name__ == '__main__':
    """starts here"""
    # Calculate directly
    start = time.time()
    print(lexographic_permutation("0123456789", 1000000 - 1)) # 2783915460
    print(time.time() - start) # 0.0001 sec

    # Calculate incrementally
    start = time.time()
    count = 1
    for p in lexilogical_permutation_generator("0123456789"):
        if count == 1000000:
            print(p)
            break
        count += 1
    print(time.time() - start) # 2.24578 sec
