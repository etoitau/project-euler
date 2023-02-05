# A number chain is created by continuously adding the square 
# of the digits in a number to form a new number until it has been 
# seen before.
# For example,
# 44 → 32 → 13 → 10 → 1 → 1
# 85 → 89 → 145 → 42 → 20 → 4 → 16 → 37 → 58 → 89
# Therefore any chain that arrives at 1 or 89 will become stuck 
# in an endless loop. What is most amazing is that EVERY starting 
# number will eventually arrive at 1 or 89.
# How many starting numbers below ten million will arrive at 89?
# Result: 8581146

from typing import Callable, Generator, Set, List, Tuple, Dict
import time
import sys
import math
from collections import OrderedDict

sys.path.append(".")
from util import count_digits, int_to_int_array
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))


def get_memo(limit: int) -> List[int]:
    # the value at index i will tell whether i ends up at 1 or 89
    # they start as -1 except for 1 and 89, themselves
    size = limit
    # note if the limit is fairly small, the chain may include
    # values larger than the limit. e.g. if the limit is 100, 99 -> 162
    next = count_digits(size) * 81
    while next > size:
        size = next
        next = count_digits(size) * 81
    memo = [-1] * size
    memo[1] = 1
    memo[89] = 89
    return memo

def recur(next: int, memo: List[int]) -> int:
    if memo[next] == 1:
        return 1
    if memo[next] == 89:
        return 89
    memo[next] = recur(sum([ d * d for d in int_to_int_array(next) ]), memo)
    return memo[next]

def solve(limit: int) -> int:
    memo = get_memo(limit)
    count = 0
    for n in range(1, limit):
        if recur(n, memo) == 89:
            count += 1
    return count

if __name__ == '__main__':
    """ starts here """
    start = time.time()
    limit = 10000000 # 10000000
    print(solve(limit)) # 8581146
    print(time.time() - start) # 19.75
