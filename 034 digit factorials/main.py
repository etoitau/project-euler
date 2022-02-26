# 145 is a curious number, as 1! + 4! + 5! = 1 + 24 + 120 = 145.
# Find the sum of all numbers which are equal to the sum of the 
# factorial of their digits.
# Note: As 1! = 1 and 2! = 2 are not sums they are not included.
# Result: 40730

import math
from typing import Set, List, Tuple, Dict
from functools import reduce
import time
import sys
sys.path.append(".")
from util import factorials, int_to_int_array
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))


if __name__ == '__main__':
    """starts here"""
    start = time.time()
    # precompute factorials we'll use a lot
    facts = factorials(9)
    # We know the answers will all be <= 7 * 9! because you can't
    # get an eight digit result from adding the factorial of
    # eight 9s.
    limit = 7 * facts[9] + 1
    result = 0
    for n in range(3, limit):
        if n == sum([ facts[d] for d in int_to_int_array(n) ]):
            result += n
    print(result) # 40730
    print(time.time() - start) # 6.075 sec
