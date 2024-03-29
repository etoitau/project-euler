# Consider all integer combinations of a^b for 2 ≤ a ≤ 5 and 2 ≤ b ≤ 5:
# 2^2=4, 2^3=8, 2^4=16, 2^5=32
# 3^2=9, 3^3=27, 3^4=81, 3^5=243
# 4^2=16, 4^3=64, 4^4=256, 4^5=1024
# 5^2=25, 5^3=125, 5^4=625, 5^5=3125
# If they are then placed in numerical order, with any repeats removed, 
# we get the following sequence of 15 distinct terms:
# 4, 8, 9, 16, 25, 27, 32, 64, 81, 125, 243, 256, 625, 1024, 3125
# How many distinct terms are in the sequence generated by a^b 
# for 2 ≤ a ≤ 100 and 2 ≤ b ≤ 100?
# Result: 9183

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
    n = 100
    start = time.time()
    values = set()
    for a in range(2, n + 1):
        curr = a
        for i in range(2, n + 1):
            curr *= a
            values.add(curr)
    print(len(values)) # 9183
    print(time.time() - start) # 0.004 sec
