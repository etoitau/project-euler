# https://projecteuler.net/problem=64
# How many continued fractions for N <= 10,000 have an odd period?
# Result: 1322

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
    for n in range(2, 10001):
        # set up
        a0 = math.floor(math.sqrt(n))
        m = a0
        d = 1

        # first
        d = n - (m * m) // d
        if not d:
            # n is perfect square, skip
            continue
        a = (a0 + m) // d
        m = a * d - m
        cycle_start = (d, a, m)

        cycle = 1
        while True:
            d = (n - (m * m)) // d
            a = (a0 + m) // d
            m = a * d - m
            if (d, a, m) == cycle_start:
                break
            cycle += 1
        if cycle % 2:
            count += 1
    return count

if __name__ == '__main__':
    """ starts here """
    start = time.time()
    print(solve()) # 1322
    print(time.time() - start) # 0.093 sec
