# The number 145 is well known for the property that the sum of the 
# factorial of its digits is equal to 145:
# 1! + 4! + 5! = 1 + 24 + 120 = 145
# Perhaps less well known is 169, in that it produces the longest 
# chain of numbers that link back to 169; it turns out that there 
# are only three such loops that exist:
# 169 → 363601 → 1454 → 169
# 871 → 45361 → 871
# 872 → 45362 → 872
# It is not difficult to prove that EVERY starting number will 
# eventually get stuck in a loop. For example,
# 69 → 363600 → 1454 → 169 → 363601 (→ 1454)
# 78 → 45360 → 871 → 45361 (→ 871)
# 540 → 145 (→ 145)
# Starting with 69 produces a chain of five non-repeating terms, 
# but the longest non-repeating chain with a starting number below 
# one million is sixty terms.
# How many chains, with a starting number below one million, 
# contain exactly sixty non-repeating terms?
# Result: 402

import math
from typing import Callable, Generator, Set, List, Tuple, Dict
import time
import sys
sys.path.append(".")
from util import factorials, int_to_int_array
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

def solve() -> int:
    limit = 1000000
    facts = factorials(9)
    # -2 will mean not visited yet
    # -1 will mean visited in the current path traversal
    # otherwise, value is the path length from that number/index
    # largest possible number we'll encounter is six digits, all nines
    # = 9! * 6 = 2177280
    memo = [ -2 ] * 2177281
    for n in range(limit):
        if memo[n] < 0:
            path_length(n, memo, facts)
    count = 0
    for i in range(limit):
        if memo[i] == 60:
            count += 1
    return count

def path_length(start: int, memo: List[int], facts: List[int]) -> None:
    next = add_facts(start, facts)
    if next == start:
        memo[next] = 0
        return
    if memo[next] == -1:
        # next is already visited, found loop
        # explore loop, count length
        loop = [ next ]
        while loop[-1] != start:
            loop.append(add_facts(loop[-1], facts))
        loop_len = len(loop)
        # set length to all in loop
        for n in loop:
            memo[n] = loop_len
        return
    if memo[next] == -2:
        # next is unexplored
        # mark current as explored, but unknown
        memo[start] = -1
        path_length(next, memo, facts)
        # if start was part of loop, will already have value, else...
        if memo[start] == -1:
            memo[start] = memo[next] + 1
        return
    if memo[next] > -1:
        # we already have a length for next
        memo[start] = memo[next] + 1
    

def add_facts(n: int, facts: List[int]):
    return sum([ facts[d] for d in int_to_int_array(n) ])

if __name__ == '__main__':
    """ starts here """
    start = time.time()
    print(solve()) # 402
    print(time.time() - start) # 2.314 sec
