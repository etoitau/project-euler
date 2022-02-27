# Take the number 192 and multiply it by each of 1, 2, and 3:
# 192 × 1 = 192
# 192 × 2 = 384
# 192 × 3 = 576
# By concatenating each product we get the 1 to 9 pandigital, 
# 192384576. We will call 192384576 the concatenated product of 
# 192 and (1,2,3)
# The same can be achieved by starting with 9 and multiplying by 
# 1, 2, 3, 4, and 5, giving the pandigital, 918273645, which is 
# the concatenated product of 9 and (1,2,3,4,5).

# What is the largest 1 to 9 pandigital 9-digit number that can 
# be formed as the concatenated product of an integer with 
# (1,2, ... , n) where n > 1?
# Result: 932718654

import math
from typing import Set, List, Tuple, Dict
from functools import reduce
import time
import sys
sys.path.append(".")
from util import PrimeMachine, get_palindromes, int_array_to_int, int_to_int_array, is_palindrome, permute_pick_n, rotations, to_array_base
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))


if __name__ == '__main__':
    """starts here"""
    start = time.time()
    # we already have 918273645, so answer must be larger than that
    # start with mult by 1, so number must start with 9
    # How many digits? 
    # can't be two, terms would have 2, 3, 3... digits
    # can't be three, terms would have 3, 4, 4....
    # must be four, terms would have 4, 5
    # 9abc -> 9abc1defg so 
    # test four digit numbers starting with 9 and not containing 1
    max = 918273645
    for digs in permute_pick_n([2, 3, 4, 5, 6, 7, 8], 3):
        begin = [9] + digs
        end = int_to_int_array(int_array_to_int(begin) * 2)
        used = set(begin)
        used.update(end)
        used.add(0)
        if len(used) == 10:
            as_num = int_array_to_int(begin + end)
            if as_num > max:
                max = as_num
    print(max) # 932718654
    print(time.time() - start) # 0.002 sec
