# An irrational decimal fraction is created by concatenating the positive integers:
# 0.123456789101112131415161718192021...
# It can be seen that the 12th digit of the fractional part is 1.
# If dn represents the nth digit of the fractional part, find the value of 
# the following expression.
# d1 × d10 × d100 × d1000 × d10000 × d100000 × d1000000
# Result: 210

import math
from typing import Set, List, Tuple, Dict
from functools import reduce
import time
import sys
sys.path.append(".")
from util import rotations
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

def champ_digit(n: int) -> int:
    # 0 index
    n -= 1
    # how many digits is the number we're looking for?
    start_number = 1
    # 0 index
    start_digit = 0
    # we're in the region of numbers with this many digits
    digits_per = 1
    # there are this many numbers with this many digits
    quant = 9
    while True:
        delta = digits_per * quant
        if start_digit + delta > n:
            break
        start_number += quant
        start_digit += delta
        digits_per += 1
        quant *= 10
    # what number is it?
    number = start_number + (n - start_digit) // digits_per
    # what character of the number?
    char_index = (n - start_digit) % digits_per
    return int(str(number)[char_index])


if __name__ == '__main__':
    """starts here"""
    start = time.time()
    ds = [ 1, 10, 100, 1000, 10000, 100000, 1000000 ]
    prod = 1
    for d in ds:
        prod *= champ_digit(d)
    print(prod) # 210
    print(time.time() - start) # 0.001 sec
