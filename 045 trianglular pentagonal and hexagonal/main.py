# Triangle, pentagonal, and hexagonal numbers are generated 
# by the following formulae:
# Triangle	 	Tn=n(n+1)/2	 	1, 3, 6, 10, 15, ...
# Pentagonal	 	Pn=n(3n−1)/2	 	1, 5, 12, 22, 35, ...
# Hexagonal	 	Hn=n(2n−1)	 	1, 6, 15, 28, 45, ...
# It can be verified that T285 = P165 = H143 = 40755.
# Find the next triangle number that is also pentagonal 
# and hexagonal.
# Result: 1533776805

from itertools import permutations
import math
from typing import Set, List, Tuple, Dict
from functools import reduce
import time
import sys
sys.path.append(".")
from util import is_hexagonal_number, is_pentagonal_number
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
    
if __name__ == '__main__':
    """starts here"""
    start = time.time()
    t = 285
    tn = 40755
    while True:
        t += 1
        tn += t
        if is_hexagonal_number(tn) and is_pentagonal_number(tn):
            print(tn) # 1533776805
            break
    print(time.time() - start) # 0.111 sec
