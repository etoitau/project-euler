# Using names.txt (right click and 'Save Link/Target As...'), a 46K text file 
# containing over five-thousand first names, begin by sorting it into 
# alphabetical order. Then working out the alphabetical value for each name, 
# multiply this value by its alphabetical position in the list to obtain a 
# name score.
# For example, when the list is sorted into alphabetical order, COLIN, which 
# is worth 3 + 15 + 12 + 9 + 14 = 53, is the 938th name in the list. So, COLIN 
# would obtain a score of 938 × 53 = 49714.
# What is the total of all the name scores in the file?
# Result: 871198282

import math
from typing import Set, List, Tuple, Dict
from functools import reduce
import time
import sys
sys.path.append(".")
from util import radix_sort
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

A = ord("A") - 1 # we want A to come out as 1

def str_to_int_array(input: str) -> List[int]:
    return [ ord(c) - A for c in input.upper() ]

def get_names() -> List[str]:
    names: List[str]
    with open(os.path.join(__location__, "p022_names.txt")) as f:
        input = f.readline()
        names = input.split(",")
    return [ name.strip('" ') for name in names ]

def naive() -> int:
    names = get_names()
    names.sort()
    res = 0
    for i in range(len(names)):
        res += sum(str_to_int_array(names[i])) * (i + 1)
    return res

def with_radix() -> int:
    names = get_names()
    to_sort = [ str_to_int_array(name) for name in names ]
    radix_sort(to_sort, False)
    res = 0
    for i in range(len(to_sort)):
        res += sum(to_sort[i]) * (i + 1)
    return res


if __name__ == '__main__':
    """starts here"""
    start = time.time()
    print(with_radix()) # 871198282
    print(time.time() - start) # 0.187 sec
    # Radix sort actually comes in quite a bit slower. Probably becuase
    # even though algorithmic time complexity is better, there is actually a
    # lot of overhead in copying and itterating over lists.
    start = time.time()
    print(naive()) # 871198282
    print(time.time() - start) # 0.094 sec
