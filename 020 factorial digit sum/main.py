# n! means n × (n − 1) × ... × 3 × 2 × 1
# For example, 10! = 10 × 9 × ... × 3 × 2 × 1 = 3628800,
# and the sum of the digits in the number 10! 
# is 3 + 6 + 2 + 8 + 8 + 0 + 0 = 27.
# Find the sum of the digits in the number 100!
# Result: 648

import math
from typing import Set, List, Tuple, Dict
from functools import reduce
import time
import sys
sys.path.append(".")
from util import Node


if __name__ == '__main__':
    """starts here"""
    # check first of each month and count
    start = time.time()
    print(sum([ int(d) for d in str(math.factorial(100))])) # 648
    print(time.time() - start) # 0.0005 sec
