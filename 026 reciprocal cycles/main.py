# A unit fraction contains 1 in the numerator. 
# The decimal representation of the unit fractions with 
# denominators 2 to 10 are given:
# 1/2	= 	0.5
# 1/3	= 	0.(3)
# 1/4	= 	0.25
# 1/5	= 	0.2
# 1/6	= 	0.1(6)
# 1/7	= 	0.(142857)
# 1/8	= 	0.125
# 1/9	= 	0.(1)
# 1/10	= 	0.1
# Where 0.1(6) means 0.166666..., and has a 1-digit recurring cycle. 
# It can be seen that 1/7 has a 6-digit recurring cycle.
# Find the value of d < 1000 for which 1/d contains the longest 
# recurring cycle in its decimal fraction part.
# Result: 

import math
from typing import Set, List, Tuple, Dict
from functools import reduce
import time
import sys
sys.path.append(".")
from util import fibonacci_generator
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

def decimal_places_generator(num: int, denom: int):
    carry = num * 10
    while True:
        d = carry // denom
        rem = carry % denom
        yield d, rem
        carry = rem * 10

def get_decimal_cycle(d):
    memo = {}
    gen = decimal_places_generator(1, d)
    count = 0
    while True:
        pair = next(gen)
        if pair in memo:
            return count - memo[pair]
        else: 
            memo[pair] = count
        count += 1

if __name__ == '__main__':
    """starts here"""
    start = time.time()
    max_cycle = 1
    max_divisor = 2
    for i in range(2, 1000):
        cycle = get_decimal_cycle(i)
        if cycle > max_cycle:
            max_cycle = cycle
            max_divisor = i
    print(max_divisor) # 983
    print(time.time() - start) # 0.042 sec
