# The nth term of the sequence of triangle numbers is given by, tn = ½n(n+1); 
# so the first ten triangle numbers are:
# 1, 3, 6, 10, 15, 21, 28, 36, 45, 55, ...
# By converting each letter in a word to a number corresponding to its 
# alphabetical position and adding these values we form a word value. 
# For example, the word value for SKY is 19 + 11 + 25 = 55 = t10. 
# If the word value is a triangle number then we shall call the word a triangle word.

# Using words.txt (right click and 'Save Link/Target As...'), 
# a 16K text file containing nearly two-thousand common English words, 
# how many are triangle words?
# Result: 162

import math
from typing import Set, List, Tuple, Dict
from functools import reduce
import time
import sys
sys.path.append(".")
from util import is_triangle_number, sum_character_numbers
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

def get_names() -> List[str]:
    names: List[str]
    with open(os.path.join(__location__, "p042_words.txt")) as f:
        input = f.readline()
        names = input.split(",")
    return [ name.strip('" ') for name in names ]
    
if __name__ == '__main__':
    """starts here"""
    start = time.time()
    count = 0
    for name in get_names():
        if is_triangle_number(sum_character_numbers(name)):
            count += 1
    print(count) # 162
    print(time.time() - start) # 0.015 sec
