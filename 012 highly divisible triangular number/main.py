# The sequence of triangle numbers is generated by adding the natural 
# numbers. So the 7th triangle number would be 
# 1 + 2 + 3 + 4 + 5 + 6 + 7 = 28. 
# The first ten terms would be:
# 1, 3, 6, 10, 15, 21, 28, 36, 45, 55, ...
# Let us list the factors of the first seven triangle numbers:
#  1: 1
#  3: 1,3
#  6: 1,2,3,6
# 10: 1,2,5,10
# 15: 1,3,5,15
# 21: 1,3,7,21
# 28: 1,2,4,7,14,28
# We can see that 28 is the first triangle number to have over five divisors.
# What is the value of the first triangle number to have over 
# five hundred divisors?
# Result: 76576500

import math
from typing import Set, List, Tuple
from functools import reduce
import time
import sys
sys.path.append(".")
from util import prime_factors, triangle_number

def first_triangle_with_n_factors_fast(n: int) -> int:
    # Credit to https://www.mathblog.dk/triangle-number-with-more-than-500-divisors/
    # for the approach, here
    # kth triangle is k/2 * (k+1) or k * (k+1)/2
    # n divisors = ndiv(k/2) * ndiv(k+1) or ndiv(k) * ndiv((k+1)/2)
    # choose which based on which part is divisible by 2
    # note ndiv(k) is ndiv(k+1) from the last iteration
    count = 1
    k = 1
    part2 = 1 # n_divisors((k + 1) // 2) == n_divisors(1) == 1
    while count < n:
        k += 1
        if not k % 2:
            # k is even
            part1 = part2 # n_divisors(k / 2) this is part 2 from last cycle
            part2 = n_divisors(k + 1)
        else:
            part1 = part2 # n_divisors(k) this is part 2 from last cycle
            part2 = n_divisors((k + 1) // 2)
        count = part1 * part2 
    return triangle_number(k)

def first_triangle_with_n_factors(n: int) -> int:
    guess = 1
    count = 1
    while count < n:
        guess += 1
        count = n_divisors(triangle_number(guess))
    return triangle_number(guess)

def n_divisors(n: int) -> int:
    prime_factorization = prime_factors(n)
    count = 1
    for factor in prime_factorization:
        if factor == 1:
            continue
        count *= (prime_factorization[factor] + 1)
    return count


if __name__ == '__main__':
    """starts here"""
    start = time.time()
    print(first_triangle_with_n_factors_fast(500)) # 76576500
    print(time.time() - start) # 0.185 sec

    start = time.time()
    print(first_triangle_with_n_factors(500)) # 76576500
    print(time.time() - start) # 1.376 sec