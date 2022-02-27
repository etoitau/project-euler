# The decimal number, 585 = 1001001001 (binary), is palindromic 
# in both bases.
# Find the sum of all numbers, less than one million, which 
# are palindromic in base 10 and base 2.
# (Please note that the palindromic number, in either base, 
# may not include leading zeros.)
# Result: 872187

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
    result = 0
    for p in get_palindromes(6):
        # check all base 10 palindromes 6 digits or less
        if is_palindrome(to_array_base(p, 2)):
            result += p
    print(result) # 872187
    print(time.time() - start) # 0.015 sec
