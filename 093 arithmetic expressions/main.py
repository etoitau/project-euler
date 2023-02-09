# By using each of the digits from the set, {1, 2, 3, 4}, exactly once, 
# and making use of the four arithmetic operations (+, −, *, /) and 
# brackets/parentheses, it is possible to form different positive 
# integer targets.
# For example,
# 8 = (4 * (1 + 3)) / 2
# 14 = 4 * (3 + 1 / 2)
# 19 = 4 * (2 + 3) − 1
# 36 = 3 * 4 * (2 + 1)
# Note that concatenations of the digits, like 12 + 34, are not allowed.
# Using the set, {1, 2, 3, 4}, it is possible to obtain thirty-one 
# different target numbers of which 36 is the maximum, and each of the 
# numbers 1 to 28 can be obtained before encountering the first 
# non-expressible number.
# Find the set of four distinct digits, a < b < c < d, for which the 
# longest set of consecutive positive integers, 1 to n, can be obtained, 
# giving your answer as a string: abcd.
# Result: 1258

from itertools import permutations
from tkinter import N
from typing import Callable, Generator, Set, List, Tuple, Dict
import time
import sys
import math
from operator import add, sub, mul, truediv as div

sys.path.append(".")
from util import combinations_no_repeats, permute, combinations_in_order
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

# Operator type
O_TYPE = Callable[[float, float], float]

# The operations at our disposal
operations: List[O_TYPE] = [add, sub, mul, div]

# We can use parenthesis to enforce any order of operations we want
# Create functions for each of those. 
# e.g. 021 means combine a and b first, then c and d, then the result of those two
# ops is our current list of three operations
def order012(a: float, b: float, c: float, d: float, ops: List[O_TYPE]) -> float:
    return ops[2](ops[1](ops[0](a, b), c), d)

def order021(a: float, b: float, c: float, d: float, ops: List[O_TYPE]) -> float:
    return ops[1](ops[0](a, b), ops[2](c, d))

def order102(a: float, b: float, c: float, d: float, ops: List[O_TYPE]) -> float:
    return ops[2](ops[0](a, ops[1](b, c)), d)

def order120(a: float, b: float, c: float, d: float, ops: List[O_TYPE]) -> float:
    return ops[0](a, ops[2](ops[1](b, c), d))

def order210(a: float, b: float, c: float, d: float, ops: List[O_TYPE]) -> float:
    return ops[0](a, ops[1](b, ops[2](c, d)))

def do_adds(a: float, b: float, c: float, d: float, \
        ops: List[O_TYPE], found: Set[int]) -> None:
    # For a given list of values and list of operations
    # apply those operations using each possible order of operations
    # If the result is valid, add it to the given set of results
    for func in [order012, order021, order102, order120, order210]:
        try:
            res = func(a, b, c, d, ops)
            if res > 0 and (isinstance(res, int) or res.is_integer()):
                found.add(int(res))
        except ZeroDivisionError:
            continue

def solve() -> str:
    farthest = 31
    best_set = [1, 2, 3, 4]
    # precalc all possible sets of operations
    op_permutations: List[List[O_TYPE]] = []
    for o_combo in combinations_in_order(operations, 3):
        # For all combinations of three operations, including repeats
        for o_perm in permute(o_combo):
            # Note permute modifies the passed list in-place, so make copies
            op_permutations.append(list(o_perm))
    
    for numbers in combinations_no_repeats([n for n in range(1, 10)], 4):
        # for each combo of 4 elements from 1-9, no repeats
        # Set of the integers we can get from this set of numbers
        found_numbers: Set[int] = set()
        for [a, b, c, d] in permute(numbers):
            # for each permutation of combo
            for ops in op_permutations:
                # for each way we can pick operators
                do_adds(a, b, c, d, ops, found_numbers)
        # See how far we can go without being able to make an integer
        # while n in set, n += 1
        # check against max
        n = 1
        while n in found_numbers:
            n += 1
        if (n - 1) > farthest:
            farthest = n - 1
            best_set = numbers        
    return "".join(sorted([str(n) for n in best_set]))

if __name__ == '__main__':
    """ starts here """
    start = time.time()
    print(solve()) # 1258
    print(time.time() - start) # 1.39
