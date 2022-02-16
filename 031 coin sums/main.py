# In the United Kingdom the currency is made up of pound (£) and pence (p). 
# There are eight coins in general circulation:
# 1p, 2p, 5p, 10p, 20p, 50p, £1 (100p), and £2 (200p).
# It is possible to make £2 in the following way:
# 1×£1 + 1×50p + 2×20p + 1×5p + 1×2p + 3×1p
# How many different ways can £2 be made using any number of coins?
# Result: 73682

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

def knapsack(target: int, options: List[int], start_option: int = 0) -> int:
    count = 0
    for i in range(start_option, len(options)):
        if target > options[i]:
            count += knapsack(target - options[i], options, i)
        elif target == options[i]:
            count += 1
    return count

def dynamic(target: int, options: List[int]) -> int:
    # Credit to https://www.mathblog.dk/project-euler-31-combinations-english-currency-denominations/
    memo = [0] * (target + 1)
    memo[0] = 1
    for o in options:
        for i in range(o, len(memo)):
            memo[i] += memo[i - o]
    return memo[-1]

if __name__ == '__main__':
    """starts here"""
    start = time.time()
    options = [1, 2, 5, 10, 20, 50, 100, 200]
    target = 200
    print(dynamic(target, options)) # 73682
    print(time.time() - start) # 0.001 sec
    start = time.time()
    options = [1, 2, 5, 10, 20, 50, 100, 200]
    target = 200
    print(knapsack(target, options)) # 73682
    print(time.time() - start) # 1.822 sec
