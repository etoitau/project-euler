# For a number written in Roman numerals to be considered valid there 
# are basic rules which must be followed. Even though the rules allow 
# some numbers to be expressed in more than one way there is always a 
# "best" way of writing a particular number.
# For example, it would appear that there are at least six ways of 
# writing the number sixteen:
# IIIIIIIIIIIIIIII
# VIIIIIIIIIII
# VVIIIIII
# XIIIIII
# VVVI
# XVI
# However, according to the rules only XIIIIII and XVI are valid, 
# and the last example is considered to be the most efficient, 
# as it uses the least number of numerals.
# The 11K text file, roman.txt contains one thousand numbers 
# written in valid, but not necessarily minimal, Roman numerals; 
# see About... Roman Numerals for the definitive rules for 
# this problem.
# Numerals must be arranged in descending order of size.
# M, C, and X cannot be equalled or exceeded by smaller denominations.
# D, L, and V can each only appear once.
# Only one I, X, and C can be used as the leading numeral in part of a subtractive pair.
# I can only be placed before V and X.
# X can only be placed before L and C.
# C can only be placed before D and M
# Find the number of characters saved by writing each of these 
# in their minimal form.
# Note: You can assume that all the Roman numerals in the 
# file contain no more than four consecutive identical units.
# Result: 743

from typing import Callable, Generator, Set, List, Tuple, Dict
import time
import sys
import math
from collections import OrderedDict

sys.path.append(".")
from util import combinations_in_order
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))


r_to_a = {
    "I": 1,
    "V": 5,
    "X": 10,
    "L": 50,
    "C": 100,
    "D": 500,
    "M": 1000
}

a_to_r: Dict[int, str] = OrderedDict(reversed([
    (1, "I"),
    (4, "IV"),
    (5, "V"),
    (9, "IX"),
    (10, "X"),
    (40, "XL"),
    (50, "L"),
    (90, "XC"),
    (100, "C"),
    (400, "CD"),
    (500, "D"),
    (900, "CM"),
    (1000, "M")
]))

roman_values = [ v for v in a_to_r.keys() ]


def roman_to_arabic(roman: str) -> int:
    # start at the end
    i = len(roman) - 1
    # accumulate value here
    arabic = 0
    # to keep track of whether the current character should be subtractive
    sign = 1 
    # initialize to 0 so the first character is greater and we
    # start with addition
    last = 0
    while i >= 0:
        current = r_to_a[roman[i]]
        # note if current == last we keep the same sign
        if current > last:
            sign = 1
        elif current < last:
            sign = -1
        arabic += current * sign
        last = current
        i -= 1
    return arabic

def arabic_to_roman(n: int) -> str:
    # Since our dictionaries include subtractive pairs, we can just
    # use a greedy algorithm and use the highest-value roman
    # digit we can.
    roman = ""
    i = 0
    while n != 0:
        if n < roman_values[i]:
            i += 1
            continue
        n -= roman_values[i]
        roman += a_to_r[roman_values[i]]
    return roman

def solve() -> int:
    char_count = 0
    with open(os.path.join(__location__, "p089_roman.txt")) as f:
        for line in f:
            input = line.rstrip('\n')
            # note input length
            # convert to int
            # convert to roman
            # note final length
            # add difference to counter
            char_count += len(input) - len(arabic_to_roman(roman_to_arabic(input)))
    return char_count


if __name__ == '__main__':
    """ starts here """
    examples = {
        "I": 1,
        "II": 2,
        "III": 3,
        "IV": 4,
        "V": 5,
        "VI": 6,
        "VII": 7,
        "CMXCIX": 999,
        "MCMLXXXVIII": 1988
    }
    start = time.time()
    
    # for r in examples.keys():
    #     assert roman_to_arabic(r) == examples[r]
    # print(arabic_to_roman(1988))
    print(solve()) # 743
    print(time.time() - start) # 0.006
