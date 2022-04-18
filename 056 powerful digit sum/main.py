# A googol (10^100) is a massive number: one followed by one-hundred zeros; 
# 100^100 is almost unimaginably large: one followed by two-hundred zeros. 
# Despite their size, the sum of the digits in each number is only 1.
# Considering natural numbers of the form, ab, where a, b < 100, what is the 
# maximum digital sum?
# Result: 972

from typing import Set, List, Tuple, Dict
import time
import sys
sys.path.append(".")
from util import digital_sum
import os
import math

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

    
if __name__ == '__main__':
    """starts here"""
    start = time.time()
    result = 0
    base_limit = 100
    exp_limit = 100
    for b in range(2, base_limit):
        n = b
        for e in range(2, exp_limit):
            n *= b
            digit_sum = digital_sum(n)
            if result < digit_sum:
                result = digit_sum
    print(result) # 972
    print(time.time() - start) # 0.132 sec
