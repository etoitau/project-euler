# If the numbers 1 to 5 are written out in words: one, two, three, four, five, then there 
# are 3 + 3 + 5 + 4 + 4 = 19 letters used in total.
# If all the numbers from 1 to 1000 (one thousand) inclusive were written out in words, 
# how many letters would be used?
# NOTE: Do not count spaces or hyphens. For example, 342 (three hundred and forty-two) 
# contains 23 letters and 115 (one hundred and fifteen) contains 20 letters. The use of "and" when writing out numbers is in compliance with British usage.
# Result: 

import math
from typing import Set, List, Tuple, Dict
from functools import reduce
import time
import sys
sys.path.append(".")
from util import prime_factors, triangle_number


dictionary = {
    0: 0,
    1: 3,
    2: 3,
    3: 5,
    4: 4,
    5: 4,
    6: 3,
    7: 5,
    8: 5,
    9: 4,
    10: 3,
    11: 6,
    12: 6,
    13: 8,
    14: 8,
    15: 7,
    16: 7,
    17: 9, 
    18: 8, 
    19: 8, 
    20: 6,
    30: 6,
    40: 5,
    50: 5,
    60: 5,
    70: 7,
    80: 6,
    90: 6,
    1000: 11
}

hundred = 7
an = 3

def letter_count_all_through(n: int) -> int:
    return sum([ letter_count(d) for d in range(n + 1) ])

def letter_count(n: int) -> int:
    if n in dictionary:
        return dictionary[n]
    count = 0
    last_two = n % 100
    if last_two in dictionary:
        # 0-19
        count += dictionary[last_two]
    else:
        last_one = last_two % 10
        count += dictionary[last_one]
        count += dictionary[last_two - last_one]
    n //= 100
    if n:
        count += hundred
        if last_two:
            count += an
    count += dictionary[n]
    return count

if __name__ == '__main__':
    """starts here"""
    n = 1000
    start = time.time()
    print(letter_count_all_through(n)) # 21124
    print(time.time() - start) # 0.0008 sec
