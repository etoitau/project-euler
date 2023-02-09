# The proper divisors of a number are all the divisors excluding the 
# number itself. For example, the proper divisors of 28 are 1, 2, 4, 7, 
# and 14. As the sum of these divisors is equal to 28, we call it a 
# perfect number.
# Interestingly the sum of the proper divisors of 220 is 284 and the 
# sum of the proper divisors of 284 is 220, forming a chain of two 
# numbers. For this reason, 220 and 284 are called an amicable pair.
# Perhaps less well known are longer chains. For example, starting 
# with 12496, we form a chain of five numbers:
# 12496 → 14288 → 15472 → 14536 → 14264 (→ 12496 → ...)
# Since this chain returns to its starting point, it is called an 
# amicable chain.
# Find the smallest member of the longest amicable chain with no 
# element exceeding one million.
# Result: 14316

from typing import Callable, Generator, Set, List, Tuple, Dict
import time
import sys
import math
from collections import OrderedDict

sys.path.append(".")
from util import factors_to_divisors, PrimeMachine
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))


def next(n: int, pm: PrimeMachine) -> int: 
    # use existing functions for finding the proper divisors
    return sum(factors_to_divisors(pm.prime_factors(n)))

def solve(limit: int) -> int:
    # note all values we don't need to explore again
    visited: Set[int] = set()
    # the values we've reached from the current starting point
    loop_visited: Set[int] = set()
    # a tuple of the lowest value of the longest loop we've seen, 
    # and the length of that loop
    longest: Tuple[int, int] = (12496, 5)
    # the PrimeMachine will keep track of known primes and help with 
    # factorization and getting proper divisors
    pm = PrimeMachine(limit)
    # we know all primes are not part of a loop, because they all go to 1
    visited.update(pm.prime_set)
    for n in range(4, limit):
        if n in visited:
            continue
        # keep track of where each value leads in the current path
        loop_visited: Dict[int, int] = dict()
        loop_visited[n] = next(n, pm)
        visited.add(n)
        found_loop = True
        next_node = loop_visited[n]
        while next_node not in loop_visited:
            # loop will continue until:
            #   we find a loop (next_node in visited)
            #   we find a value we've seen before
            #   we find a value outside our given limit
            if next_node in visited:
                found_loop = False
                break
            visited.add(next_node)
            if next_node >= limit:
                found_loop = False
                break
            loop_visited[next_node] = next(next_node, pm)
            next_node = loop_visited[next_node]
        if found_loop:
            # found a loop, follow it and count how long 
            # and note smallest value
            start = next_node
            size = 1
            min = start
            next_node = loop_visited[next_node]
            while next_node != start:
                if next_node < min:
                    min = next_node
                size += 1
                next_node = loop_visited[next_node]
            if size > longest[1]:
                # if a new longest loop, save it
                longest = (min, size)
    return longest[0]

if __name__ == '__main__':
    """ starts here """
    start = time.time()
    limit = 10000000 # 1000000
    print(solve(limit)) # 14316
    print(time.time() - start) # 1843
