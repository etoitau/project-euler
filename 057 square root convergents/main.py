# It is possible to show that the square root of two can be expressed as 
# an infinite continued fraction.
# By expanding this for the first four iterations, we get:
# 1 + 1/2 = 3/2 = 1.5
# 1 + 1/(2 + 1/2) = 7/8 = 1.4
# 1 + 1/(2 + 1/(2 + 1/2)) = 17/12 = 1.4166
# 1 + 1/(2 + 1/(2 + 1/(2 + 1/2))) = 41/29 = 1.41379
# The next three expansions are 99/70, 239/169, and 577/408
# but the eighth expansion, 1393/985
# is the first example where the number of digits in the numerator 
# exceeds the number of digits in the denominator.
# In the first one-thousand expansions, how many fractions contain a 
# numerator with more digits than the denominator?
# Result: 153

from typing import Set, List, Tuple, Dict
import time
import sys
sys.path.append(".")
from util import Frac, count_digits, frac_invert
import os
import math

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

    
if __name__ == '__main__':
    """starts here"""
    start = time.time()
    count = 0
    div = Frac(2)
    for i in range(1, 1000):
        # div is the divisor of the second term of 1 + 1/...
        # The divisor of the next expansion is 2 + 1 / (the previous divisor)
        div = Frac(2 * div.n + div.d, div.n)
        # The next approximation
        app = Frac(1).add(frac_invert(div), True)
        if count_digits(app.n) > count_digits(app.d):
            count += 1
    print(count) # 153
    print(time.time() - start) # 0.162 sec
