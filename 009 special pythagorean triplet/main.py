# A Pythagorean triplet is a set of three natural numbers, a < b < c, 
# for which, a^2 + b^2 = c^2
# For example, 3^2 + 4^2 = 9 + 16 = 25 = 5^2.
# There exists exactly one Pythagorean triplet for which a + b + c = 1000.
# Find the product abc.
# Result: 31875000, from (200, 375, 425)

import math
from typing import Set, List, Tuple
from functools import reduce
import time
import sys
sys.path.append(".")
from util import nth_prime

def triplet_with_sum(n: int) -> Tuple[int, int, int]:
    count = 0
    # cache squares of numbers in range
    squares = [ int(i * i) for i in range(n - 2) ]
    max_a = (n - 3) // 3 # 332
    for a in range(1, max_a + 1):
        # b has to be bigger than a, and a + b > c, and a + b + c = n
        # b > c - a, b > (n - a - b) - a
        min_b = max(a + 1, (n - 2 * a) // 2)
        # c is at least 1 more than b, and a + b + c = n
        # b + (b + 1) = n - a
        max_b = (n - 1 - a) // 2
        for b in range (min_b, max_b + 1):
            c = n - a - b
            if squares[a] + squares[b] > squares[c]:
                break
            elif squares[a] + squares[b] == squares[c]:
                return (a, b, c)
    return (0, 0, 0)

if __name__ == '__main__':
    """starts here"""
    n = 1000
    start = time.time()
    trip = triplet_with_sum(n)
    print(trip)
    print(trip[0] * trip[1] * trip[2])
    print(time.time() - start) # 0.003 sec
