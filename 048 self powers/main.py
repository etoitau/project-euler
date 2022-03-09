# The series, 1^1 + 2^2 + 3^3 + ... + 10^10 = 10405071317.
# Find the last ten digits of the series, 1^1 + 2^2 + 3^3 + ... + 1000^1000.
# Result: 9110846700

from itertools import permutations
import math
from typing import Set, List, Tuple, Dict
from functools import reduce
import time
import sys
sys.path.append(".")
from util import PrimeMachine
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
    
if __name__ == '__main__':
    """starts here"""
    start = time.time()
    # We only need the last ten digits, so we can add each term % 10000000000
    # We already have the sum through 10
    # We dont need to add any where n % 10 == 0 because that term
    # will end in over 10 0s
    result = 405071317
    mask = 10000000000
    for n in range(11, 1000):
        if not n % 10:
            continue
        result += n**n % mask
    print(result % mask) # 9110846700
    print(time.time() - start) # 0.012 sec
