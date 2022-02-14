# Starting with the number 1 and moving to the right in a clockwise direction a 5 by 5 spiral is formed as follows:
# 21 22 23 24 25
# 20  7  8  9 10
# 19  6  1  2 11
# 18  5  4  3 12
# 17 16 15 14 13
# It can be verified that the sum of the numbers on the diagonals is 101.
# What is the sum of the numbers on the diagonals in a 1001 by 1001 spiral formed in the same way?
# Result: 669171001

import math
from typing import Set, List, Tuple, Dict
from functools import reduce
import time
import sys
sys.path.append(".")
from util import PrimeMachine, fibonacci_generator
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

if __name__ == '__main__':
    """starts here"""
    start = time.time()
    n = 1001
    total = 1
    value = 1
    for side_length in range(3, n + 1, 2):
        for i in range(4):
            value += (side_length - 1)
            total += value
    print(total) # 669171001
    print(time.time() - start) # 0.001 sec
