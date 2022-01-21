# 2^15 = 32768 and the sum of its digits is 3 + 2 + 7 + 6 + 8 = 26.
# What is the sum of the digits of the number 2^1000?
# Result: 1366

import math
from typing import Set, List, Tuple, Dict
from functools import reduce
import time
import sys
sys.path.append(".")
from util import prime_factors, triangle_number

def sum_digits_power_two(n: int) -> int:
    return sum([ int(d) for d in str(1 << n) ])

if __name__ == '__main__':
    """starts here"""
    n = 1000
    start = time.time()
    print(sum_digits_power_two(n)) # 1366
    print(time.time() - start) # 0.0002 sec
