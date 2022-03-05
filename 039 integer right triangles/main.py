# If p is the perimeter of a right angle triangle with integral 
# length sides, {a,b,c}, there are exactly three solutions for 
# p = 120.
# {20,48,52}, {24,45,51}, {30,40,50}
# For which value of p ≤ 1000, is the number of solutions maximised?
# Result: 840

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


if __name__ == '__main__':
    """starts here"""
    start = time.time()
    limit = 1000
    freq = [0] * (limit + 1)
    # cache squares of numbers in range
    squares = [ int(i * i) for i in range(limit - 3) ]
    max_a = limit // 3  - 1 # 332
    for a in range(1, max_a + 1):
        # b > a
        min_b = a + 1
        # a + b + c <= limit, min_c = b +1
        # max_b = limit - a - (max_b + 1)
        # 2 * max_b = limit - a - 1
        max_b = (limit - a - 1) // 2
        for b in range(min_b, max_b + 1):
            min_c = b + 1
            # a + b + c <= limit
            # c < a + b for a triangle
            max_c = min(limit - a - b, a + b - 1)
            for c in range(min_c, max_c + 1):
                if squares[a] + squares[b] == squares[c]:
                    # if this triangle is right, increment the 
                    # count for its perimeter
                    freq[a + b + c] += 1
    # Find perimeter with max frequency
    # problem gives us one data point to start from
    max_p = 120
    max_f = 3
    for i in range(len(freq)):
        if freq[i] > max_f:
            max_f = freq[i]
            max_p = i
    print(max_p) # 840
    print(time.time() - start) # 1.866 sec
