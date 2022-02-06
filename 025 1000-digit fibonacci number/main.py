# The Fibonacci sequence is defined by the recurrence relation:
# F(n) = F(n−1) + F(n−2), where F(1) = 1 and F(2) = 1.
# Hence the first 12 terms will be:
# F(1) = 1
# F(2) = 1
# F(3) = 2
# F(4) = 3
# F(5) = 5
# F(6) = 8
# F(7) = 13
# F(8) = 21
# F(9) = 34
# F(10) = 55
# F(11) = 89
# F(12) = 144
# The 12th term, F(12), is the first term to contain three digits.
# What is the index of the first term in the Fibonacci sequence 
# to contain 1000 digits?
# Result: 4782

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

if __name__ == '__main__':
    """starts here"""
    start = time.time()
    gen = fibonacci_generator()
    n = next(gen)
    count = 0
    while len(str(n)) < 1000:
        n = next(gen)
        count += 1
    print(count) # 4782
    print(time.time() - start) # 0.031 sec
