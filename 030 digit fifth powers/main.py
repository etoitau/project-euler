# Surprisingly there are only three numbers that can be written 
# as the sum of fourth powers of their digits:
# 1634 = 1^4 + 6^4 + 3^4 + 4^4
# 8208 = 8^4 + 2^4 + 0^4 + 8^4
# 9474 = 9^4 + 4^4 + 7^4 + 4^4
# As 1 = 1^4 is not a sum it is not included.
# The sum of these numbers is 1634 + 8208 + 9474 = 19316.
# Find the sum of all the numbers that can be written as the 
# sum of fifth powers of their digits.
# Result: 443839

import math
from typing import Set, List, Tuple, Dict
from functools import reduce
import time
import sys
sys.path.append(".")
from util import combinations_in_order
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

if __name__ == '__main__':
    """starts here"""
    # Can't be one digit, min value is 2^5 = 32
    # Can't be seven digits, max value is 7 * 9^5 = 413703
    # A lot of rework if we do number by number, e.g. 123, 213, 312
    # Want combinations of 0-9
    start = time.time()
    digits = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    # Precompute powers to avoid repeat work
    to_fifth = [ n**5 for n in digits ]
    combos = combinations_in_order(digits, 6)
    # skip 000000 and 000001
    next(combos)
    next(combos)
    matches = []
    i = 0
    for combo in combos:
        sum_fifths = sum([to_fifth[c] for c in combo])
        # Order of numbers in combo doesn't matter, we just want to check
        # same quantity of each number exists in each. And can ignore 0 
        combo_str = "".join([str(c) for c in sorted(combo)]).lstrip("0")
        fifths_str = "".join(sorted(str(sum_fifths))).lstrip("0")
        if combo_str == fifths_str:
            matches.append(sum_fifths)
    print(sum(matches)) # 443839
    print(time.time() - start) # 0.021 sec
