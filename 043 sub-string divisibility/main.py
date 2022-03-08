# The number, 1406357289, is a 0 to 9 pandigital number because it is made up 
# of each of the digits 0 to 9 in some order, but it also has a rather 
# interesting sub-string divisibility property.
# Let d1 be the 1st digit, d2 be the 2nd digit, and so on. In this way, 
# we note the following:
# d2d3d4=406 is divisible by 2
# d3d4d5=063 is divisible by 3
# d4d5d6=635 is divisible by 5
# d5d6d7=357 is divisible by 7
# d6d7d8=572 is divisible by 11
# d7d8d9=728 is divisible by 13
# d8d9d10=289 is divisible by 17
# Find the sum of all 0 to 9 pandigital numbers with this property.
# Result: 16695334890

from itertools import permutations
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
    start = time.time()
    result = 0
    primes = [1, 2, 3, 5, 7, 11, 13, 17]
    for perm in permute([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]):
        works = True
        for i in range(1, 8):
            if int_array_to_int(perm[i:i+3]) % primes[i]:
                works = False
                break
        if works:
            result += int_array_to_int(perm)
    print(result) # 16695334890
    print(time.time() - start) # 12.926 sec
