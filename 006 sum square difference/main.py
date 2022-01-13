# The sum of the squares of the first ten natural numbers is 385
# The square of the sum of the first ten natural numbers is 3025
# Hence the difference between the sum of the squares of the first ten natural numbers and 
# the square of the sum is .
# Find the difference between the sum of the squares of the first one hundred natural numbers 
# and the square of the sum.
# Result: 25164150

import math
from typing import Set
from functools import reduce
import time
import sys
sys.path.append(".")
from util import triangle_number

def sum_squares(n) -> int:
    result: int = 0
    for i in range(1, n+1):
        result += int(math.pow(i, 2))
        # print(result)
    print(result)
    return result

def square_sum(n) -> int:
    print(int(math.pow(triangle_number(n), 2)))
    return int(math.pow(triangle_number(n), 2))

if __name__ == '__main__':
    """starts here"""
    n = 100
    print(square_sum(n) - sum_squares(n))
