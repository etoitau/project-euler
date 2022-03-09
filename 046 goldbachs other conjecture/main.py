# It was proposed by Christian Goldbach that every odd 
# composite number can be written as the sum of a prime and 
# twice a square.
# 9 = 7 + 2×12
# 15 = 7 + 2×22
# 21 = 3 + 2×32
# 25 = 7 + 2×32
# 27 = 19 + 2×22
# 33 = 31 + 2×12
# It turns out that the conjecture was false.
# What is the smallest odd composite that cannot be written 
# as the sum of a prime and twice a square?
# Result: 5777

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
    pm = PrimeMachine()
    n = 33
    squares = [ n**2 for n in range(100) ]
    while True:
        # only want odd
        n += 2
        if pm.is_prime(n):
            # only want coposite
            continue
        fits = False
        while squares[-1] < n / 2:
            # get more squares if needed
            squares.append(len(squares)**2)
        for p in pm:
            # for each prime less than n, see if 
            # adding 2* some square can get you n
            if p > n:
                break
            for s in squares:
                conjecture = p + 2 * s
                if conjecture > n:
                    break
                elif conjecture == n:
                    fits = True
                    break
            if fits:
                break
        if not fits:
            print(n) # 5777
            break
    print(time.time() - start) # 1.362 sec
