# The fraction 49/98 is a curious fraction, as an inexperienced mathematician in attempting to simplify 
# it may incorrectly believe that 49/98 = 4/8, which is correct, is obtained by cancelling the 9s.
# We shall consider fractions like, 30/50 = 3/5, to be trivial examples.
# There are exactly four non-trivial examples of this type of fraction, less than one in value, and 
# containing two digits in the numerator and denominator.
# If the product of these four fractions is given in its lowest common terms, find the value of the 
# denominator.
# Result: 100

import math
from typing import Set, List, Tuple, Dict
from functools import reduce
import time
import sys
sys.path.append(".")
from util import simplify_fraction
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

def digits_to_frac(top_tens, top_ones, bot_tens, bot_ones) -> Tuple[int, int]:
    return simplify_fraction(top_tens * 10 + top_ones, bot_tens * 10 + bot_ones)

if __name__ == '__main__':
    """starts here"""
    start = time.time()
    prod = [1, 1]
    for top_tens in range(1, 10):
        for top_ones in range(1, 10):
            for bot_tens in range(top_tens, 10):
                for bot_ones in range(1, 10):
                    if bot_tens == top_tens:
                        if bot_ones <= top_ones:
                            # Starting fraction needs to be < 1
                            continue
                    actually = digits_to_frac(top_tens, top_ones, bot_tens, bot_ones)
                    for top_match, top_use in [(top_tens, top_ones), (top_ones, top_tens)]:
                        for bot_match, bot_use in [(bot_tens, bot_ones), (bot_ones, bot_tens)]:
                            # That's right, six nested for loops
                            if top_match == bot_match and simplify_fraction(top_use, bot_use) == actually:
                                prod[0] *= actually[0]
                                prod[1] *= actually[1]
    print(simplify_fraction(prod[0], prod[1])[1]) # 100
    print(time.time() - start) # 0.007 sec
