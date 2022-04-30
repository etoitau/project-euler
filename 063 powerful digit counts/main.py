# The 5-digit number, 16807=7^5, is also a fifth power. 
# Similarly, the 9-digit number, 134217728=8^9, is a ninth power.
# How many n-digit positive integers exist which are also an nth power?
# Result: 49

import math
from typing import Set, List, Tuple, Dict
import time
import sys
sys.path.append(".")
from util import count_digits
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

def solve() -> int:
    count = 0
    for b in range(1, 10):
        # Note we're saying 0 doesn't count as a positive int
        # and if our base is 10 it starts with more digits than power
        # and both digits and power will increase by one with each cycle
        # so the largest possible base is 9
        p = b
        n = 1
        while True:
            digits = count_digits(p)
            if digits != n:
                break
            count += 1
            p *= b
            n += 1
    return count

if __name__ == '__main__':
    """starts here"""
    start = time.time()
    print(solve()) # 49
    print(time.time() - start) # 0.0 sec
