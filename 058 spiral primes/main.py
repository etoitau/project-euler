# Starting with 1 and spiralling anticlockwise in the following way, 
# a square spiral with side length 7 is formed.
# 37 36 35 34 33 32 31
# 38 17 16 15 14 13 30
# 39 18  5  4  3 12 29
# 40 19  6  1  2 11 28
# 41 20  7  8  9 10 27
# 42 21 22 23 24 25 26
# 43 44 45 46 47 48 49
# It is interesting to note that the odd squares lie along the bottom 
# right diagonal, but what is more interesting is that 8 out of the 13 
# numbers lying along both diagonals are prime; that is, a ratio of 8/13 ≈ 62%.
# If one complete new layer is wrapped around the spiral above, 
# a square spiral with side length 9 will be formed. 
# If this process is continued, what is the side length of the square 
# spiral for which the ratio of primes along both diagonals first falls below 10%?
# Result: 26241

from typing import Set, List, Tuple, Dict
import time
import sys
sys.path.append(".")
from util import PrimeMachine
import os
import math

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

    
if __name__ == '__main__':
    """starts here"""
    start = time.time()
    prime_count = 0
    diag_count = 1
    n = 1
    step = 2
    pm = PrimeMachine()
    while True:
        for i in range(4):
            n += step
            if i != 3 and pm.is_prime(n):
                # The last diagonal is always square and not prime
                prime_count += 1
        diag_count += 4
        if (prime_count / diag_count) < 0.1:
            break
        step += 2
    print(step + 1) # 26241
    print(time.time() - start) # 0.396 sec
