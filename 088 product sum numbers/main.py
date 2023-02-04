# A natural number, N, that can be written as the sum and product 
# of a given set of at least two natural numbers, {a1, a2, ... , ak} 
# is called a product-sum number: 
# N = a1 + a2 + ... + ak = a1 × a2 × ... × ak.
# For example, 6 = 1 + 2 + 3 = 1 × 2 × 3.
# For a given set of size, k, we shall call the smallest N with this 
# property a minimal product-sum number. The minimal product-sum 
# numbers for sets of size, k = 2, 3, 4, 5, and 6 are as follows.
# k=2: 4 = 2 × 2 = 2 + 2
# k=3: 6 = 1 × 2 × 3 = 1 + 2 + 3
# k=4: 8 = 1 × 1 × 2 × 4 = 1 + 1 + 2 + 4
# k=5: 8 = 1 × 1 × 2 × 2 × 2 = 1 + 1 + 2 + 2 + 2
# k=6: 12 = 1 × 1 × 1 × 1 × 2 × 6 = 1 + 1 + 1 + 1 + 2 + 6
# Hence for 2≤k≤6, the sum of all the minimal product-sum numbers 
# is 4+6+8+12 = 30; note that 8 is only counted once in the sum.
# In fact, as the complete set of minimal product-sum numbers for 
# 2≤k≤12 is {4, 6, 8, 12, 15, 16}, the sum is 61.
# What is the sum of all the minimal product-sum numbers for 2≤k≤12000?
# Result: 7587457

from typing import Callable, Generator, Set, List, Tuple, Dict
import time
import sys
import math

sys.path.append(".")
from util import combinations_in_order
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))


def recur(sum: int, prod: int, value: int, size: int, limit: int, results: Dict[int, int]) -> None:
    # Any pair of product and sum is a solution for 
    # some set size n, by padding with (prod - sum) 1s
    n = prod - sum + size
    if n > limit:
        # Adding more terms will just put us further over the limit
        # so bail now
        return

    if prod < results[n]:
        results[n] = prod

    # limit * 2 is the largest possible product-sum number
    # the biggest term we could add to stay under/at that is max_n
    max_n = limit * 2 // prod
    for n in range(value, max_n + 1): 
        recur(sum + n, prod * n, n, size + 1, limit, results)


def solve(limit: int) -> int:
    # 2k is a solution for any number of terms k, because of the set
    # [ k, 2, 1, 1..., 1 ] 
    # There are k - 2 1s, so the product is k * 2 
    # and the sum is k + 2 + ((k - 2) * 1) = k * 2
    results = [ 2 * k for k in range(limit + 1) ]
    recur(0, 1, 2, 0, limit, results)
    # We don't want k = 1
    # del results[1]
    # Pass through set to reduce to unique values
    return sum(set(results[2:]))

if __name__ == '__main__':
    """ starts here """
    start = time.time()
    # Examples: 6 -> 30, 12 -> 61
    limit = 12000 
    print(solve(limit)) # 7587457
    print(time.time() - start) # 0.163
