# By counting carefully it can be seen that a rectangular grid 
# measuring 3 by 2 contains eighteen rectangles:
# Although there exists no rectangular grid that contains 
# exactly two million rectangles, find the area of the grid 
# with the nearest solution.
# Result: 2772

from typing import Callable, Generator, Set, List, Tuple, Dict
import time
import sys

sys.path.append(".")
from util import Heap
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))


def count(M: int, N: int) -> int:
    """ For a M x N rectangle, how many rectangles can you make """
    total = 0
    # for each shape of rectangle at or smaller than M x N, 
    # how many can we find?
    for m in range(1, M + 1):
        for n in range(1, N + 1):
            total += (1 + M - m) * (1 + N - n)
    return total

def search_n(target: int, n: int, low_m: int, high_m: int) -> Tuple[int, int]:
    # Keeping n constant at the input, find the dimension m which gives
    # the closest approximation of the target number of rectangles.
    # We can do a binary search between the limits.
    rectangles = 0
    while low_m < high_m:
        mid = (high_m + low_m) // 2
        rectangles = count(mid, n)
        if rectangles < target:
            low_m = mid + 1
        else:
            high_m = mid
    if rectangles < target:
        other_guess = count(mid + 1, n)
        if other_guess - target < target - rectangles:
            return mid + 1, other_guess
        else:
            return mid, rectangles
    else:
        other_guess = count(mid - 1, n)
        if target - other_guess < rectangles - target:
            return mid - 1, other_guess
        else:
            return mid, rectangles

def solve(target: int) -> int:
    min_m = 2
    max_m = 2
    max_n = 2
    # Search diagonal for closest value > target
    # First quickly search up to get a max
    m = 2
    while count(m, m) < target:
        m <<= 1
    # closest is between m and m / 2
    # binary search between those limits
    low = m >> 1
    high = m
    rectangles = 0
    while low < high:
        mid = (low + high) // 2
        rectangles = count(mid, mid)
        if rectangles > target:
            high = mid
        else:
            low = mid + 1
    # if we say n <= m, we can now assume some limits
    if rectangles > target:
        max_n = mid
        min_m = mid - 1
    else:
        max_n = mid + 1
        min_m = mid
    # search at n = 1 to get max m
    # this is similar to searching the diagonal
    while count(1, max_m) < target:
        max_m <<= 1
    best_m, best_val = search_n(target, 1, min_m, max_m)
    best_n = 1
    max_m = best_m + 1
    # Now search each value of n in the range we identified
    # in the range of m we identified. Note since we're increasing
    # n, we know the found m can serve as a max m for the next iteration
    for n in range(2, max_n + 1):
        temp_m, temp_val = search_n(target, n, min_m, max_m)
        max_m = temp_m + 1
        if abs(target - temp_val) < abs(target - best_val):
            best_m, best_n, best_val = temp_m, n, temp_val
    return best_m * best_n

if __name__ == '__main__':
    """ starts here """
    start = time.time()
    print(solve(2000000)) # 2772
    print(time.time() - start) # 0.152 sec
