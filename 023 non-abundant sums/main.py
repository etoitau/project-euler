# A perfect number is a number for which the sum of its proper divisors is 
# exactly equal to the number. For example, the sum of the proper divisors of 
# 28 would be 1 + 2 + 4 + 7 + 14 = 28, which means that 28 is a perfect number.
# A number n is called deficient if the sum of its proper divisors is less than n 
# and it is called abundant if this sum exceeds n.
# As 12 is the smallest abundant number, 1 + 2 + 3 + 4 + 6 = 16, the smallest number 
# that can be written as the sum of two abundant numbers is 24. By mathematical analysis, 
# it can be shown that all integers greater than 28123 can be written as the sum of two 
# abundant numbers. However, this upper limit cannot be reduced any further by analysis 
# even though it is known that the greatest number that cannot be expressed as the sum 
# of two abundant numbers is less than this limit.
# Find the sum of all the positive integers which cannot be written as the sum of two 
# abundant numbers.
# Result: 4179871

import math
from typing import Set, List, Tuple, Dict
from functools import reduce
import time
import sys
sys.path.append(".")
from util import is_sum_of_two_from, prime_sieve, prime_factors, factors_to_divisors
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

def find_non_abundant_sum():
    # find all abundant < 28123
    limit = 28124
    known_primes = set(prime_sieve(limit))
    abundant: List[int] = []
    for i in range(12, limit):
        sum_d = sum(factors_to_divisors(prime_factors(i, known_primes)))
        if sum_d > i:
            abundant.append(i)
    # for number < 28123
    #   can it be expressed as sum of abundant?
    is_sum: List[int] = []
    for i in range(1, limit):
        if not is_sum_of_two_from(i, abundant):
            is_sum.append(i)
    return sum(is_sum)


if __name__ == '__main__':
    """starts here"""
    
    start = time.time()
    print(find_non_abundant_sum()) # 4179871
    print(time.time() - start) # 2.449 sec
