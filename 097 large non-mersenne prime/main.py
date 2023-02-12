# The first known prime found to exceed one million digits was discovered 
# in 1999, and is a Mersenne prime of the form 2^6972593−1; it contains 
# exactly 2,098,960 digits. Subsequently other Mersenne primes, of the 
# form 2p−1, have been found which contain more digits.
# However, in 2004 there was found a massive non-Mersenne prime which 
# contains 2,357,207 digits: 28433×2^7830457+1.
# Find the last ten digits of this prime number.
# Result: 

from typing import Callable, Generator, Set, List, Tuple, Dict
import time
import sys
import math
from collections import OrderedDict

sys.path.append(".")
from util import factors_to_divisors
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))


if __name__ == '__main__':
    """ starts here """
    start = time.time()
    ten = 10**10
    print((28433 * pow(2, 7830457, ten) + 1) % ten) # 8739992577
    print(time.time() - start) # 0.0002
