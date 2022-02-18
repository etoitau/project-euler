# We shall say that an n-digit number is pandigital if it makes 
# use of all the digits 1 to n exactly once; for example, the 
# 5-digit number, 15234, is 1 through 5 pandigital.
# The product 7254 is unusual, as the identity, 39 × 186 = 7254, 
# containing multiplicand, multiplier, and product is 1 through 9 
# pandigital.
# Find the sum of all products whose multiplicand/multiplier/product 
# identity can be written as a 1 through 9 pandigital.
# HINT: Some products can be obtained in more than one way so be 
# sure to only include it once in your sum.
# Result: 45228

import math
from typing import Set, List, Tuple, Dict
from functools import reduce
import time
import sys
sys.path.append(".")
from util import int_array_to_int, permute
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))


if __name__ == '__main__':
    """starts here"""
    # If using 1-9 we have nine digits total
    # an n-digit and m-digit number can multiply to a 
    # n+m digit number or a n+m+1 digit number
    # So the digits could be 1, 4, 5 
    # or 2, 3, 5, but those are the only possibilites.
    # Get each permutation of 123456789
    # Split into three parts a, b, and c of length
    # 1, 4, 5 and check if a * b = c
    # Split into three parts d, e, f of length
    # 2, 3, 5 and check if d * e = f (note f == c)
    # If equal, add to set
    start = time.time()
    digits = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    products = set()
    for perm in permute(digits):
        result = int_array_to_int(perm[5:])
        a = int_array_to_int(perm[:1])
        b = int_array_to_int(perm[1:5])
        if a * b == result:
            products.add(result)
            continue
        c = int_array_to_int(perm[:2])
        d = int_array_to_int(perm[2:5])
        if c * d == result:
            products.add(result)
    print(sum(products)) # 45228
    print(time.time() - start) # 3.620 sec
