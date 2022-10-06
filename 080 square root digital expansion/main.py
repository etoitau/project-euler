# It is well known that if the square root of a natural number is not 
# an integer, then it is irrational. The decimal expansion of such 
# square roots is infinite without any repeating pattern at all.
# The square root of two is 1.41421356237309504880..., and the 
# digital sum of the first one hundred decimal digits is 475.
# For the first one hundred natural numbers, find the total of 
# the digital sums of the first one hundred decimal digits for 
# all the irrational square roots.
# Result: 40886

import math
from typing import Callable, Generator, Set, List, Tuple, Dict
import time
import sys
sys.path.append(".")
from util import digital_sum
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))


def sqrt_digits(n: int, digits: int):
    # from Square roots by subtraction by Frazer Jarvis, learned about at
    # https://www.mathblog.dk/project-euler-80-digits-irrational-square-roots/
    # returns the square root of n to digits precision, with no decimal
    big_enough = pow(10, digits + 1)
    a = 5 * n
    b = 5
    while b < big_enough:
        if a >= b:
            a = a - b
            b += 10
        else:
            a *= 100
            b = (b // 10) * 100 + 5
    return b // 100


def solve(limit: int) -> int:
    squares: Set[int] = set()
    i = 0
    sq = 0
    while sq <= limit:
        squares.add(sq)
        sq = i * i
        i += 1

    digit_sum = 0
    for n in range(limit + 1):
        if n in squares:
            continue
        digit_sum += digital_sum(sqrt_digits(n, 100))
    return digit_sum

if __name__ == '__main__':
    """ starts here """
    start = time.time()
    print(solve(100)) # 40886
    print(time.time() - start) # 0.01 sec
