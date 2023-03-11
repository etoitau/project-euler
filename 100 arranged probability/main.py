# If a box contains twenty-one coloured discs, composed of fifteen blue 
# discs and six red discs, and two discs were taken at random, it can 
# be seen that the probability of taking two blue discs, 
# P(BB) = (15/21)×(14/20) = 1/2.
# The next such arrangement, for which there is exactly 50% chance of 
# taking two blue discs at random, is a box containing eighty-five blue 
# discs and thirty-five red discs.
# By finding the first arrangement to contain over 
# 10^12 = 1,000,000,000,000 discs in total, determine the number of 
# blue discs that the box would contain.
# Result: 756872327473

from typing import Callable, Generator, Iterable, Set, List, Tuple, Dict
import time
import sys
import math
from collections import OrderedDict, defaultdict
from string import whitespace

sys.path.append(".")
from util import binary_search_less_close, quadratic_formula, square_root_convergent_generator
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
    

def balance(b: int, r: int) -> int:
    # When the probability of picking two b is 1/2, this func will return 0
    # If b is too high, the value will be < 0. If too low, > 0
    # start with
    # (b / (r + b)) * ((b - 1) / (r + b - 1)) = 1/2
    # rearrange to: 
    # ((r + b) * (r + b - 1)) - (2 * b * (b - 1)) = 0
    # If b is too high, the value will be < 0 
    return  ((r + b) * (r + b - 1)) - (2 * b * (b - 1))

def r_given_b(b: int) -> int:
    # start with
    # (b / (r + b)) * ((b - 1) / (r + b - 1)) = 1/2
    # rearrange to:
    # -r^2 + (1 - 2 * b) * r + (b - 1) * b = 0
    # solve with quadratic formula to estimate the r closest to 
    # working for this b
    root1, root2 = quadratic_formula(-1, (1 - 2 * b), (b - 1) * b)
    return int(max(root1, root2))

def solve_slow() -> int:
    # This is correct, but would take over a day to run

    # b + r has to exceed this
    min_total = pow(10, 12)

    # find b where b + r > limit
    # b > r, so a lower bound on b is:
    b_min = min_total // 2
    b_max = min_total
    # do binary search between those limits to find limit - b - r = 0
    def at_limit(b: int) -> int:
        r = r_given_b(b)
        return (b + r) - min_total
    b = binary_search_less_close(0, b_min, b_max, at_limit)

    # from there, check each b to see if it works
    while True:
        r_close = r_given_b(b)
        if balance(b, r_close) == 0:
            return b
        b += 1


def solve() -> int:
    # b is number of blue discs, n is total number
    # (b / n) * ((b - 1) / (n - 1)) = 1/2
    # rearrange to:
    # 2 * b^2 - 2 * b - (n^2 + n)
    # from quadratic formula:
    # b = 1/2 * (1 + sqrt(1 + 2 * n^2 - 2 * n))
    # say c = sqrt(1 + 2 * n^2 - 2 * n)
    # c has to be an odd integer in order for b to be an integer
    # c^2 = 1 + 2 * n^2 - 2 * n
    # use quadratic formula to get n in terms of c
    # n = 1/2 * (1 + sqrt(2 * c^2 - 1))
    # say d = sqrt(2 * c^2 - 1)
    # d^2 = 2 * c^2 - 1
    # d^2 - 2 * c^2 = -1
    # That's a negative Pell equation for which the solutions
    # are given by every other convergent of sqrt(2)
    # Generate those until n > n_min
    # n_min = 1/2 * (1 + d_min)
    # d_min = 2 * n_min - 1
    min_total = pow(10, 12)
    # Use a boolean toggle to get every other convergent
    use = False
    for f in square_root_convergent_generator(2):
        use = not use
        if not use:
            continue
        # d and c correspond to the numerator and denominator of
        # the convergent, respectively
        d = f.n
        if d >= min_total * 2 - 1:
            return (1 + f.d) // 2

if __name__ == '__main__':
    """ starts here """
    start = time.time()
    print(solve()) # 756872327473
    print(time.time() - start) # 0.001s
