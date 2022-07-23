# Let p(n) represent the number of different ways in which n coins can be 
# separated into piles. For example, five coins can be separated into 
# piles in exactly seven different ways, so p(5)=7.
# OOOOO
# OOOO   O
# OOO   OO
# OOO   O   O
# OO   OO   O
# OO   O   O   O
# O   O   O   O   O
# Find the least value of n for which p(n) is divisible by one million.
# Result: 55374

import math
from typing import Callable, Generator, Set, List, Tuple, Dict
import time
import sys
sys.path.append(".")
from util import GeneralizedPentagonalMachine
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

def solve(div: int) -> int:
    # Return least value of n for which p(n) is divisible by div
    # This could be done similar to the previous two problems, but
    # this time try using the partition function
    # https://en.wikipedia.org/wiki/Partition_(number_theory)#Partition_function
    p = [1, 1, 2, 3]
    pentagonals = GeneralizedPentagonalMachine()
    n = 4
    
    while True:
        next_p = 0
        i = 1
        # We alternate adding and subtracting terms like ++--
        sign = True
        switch_sign = False
        while True:
            pent = pentagonals.get(i)
            if pent > n:
                break
            if sign:
                next_p += p[n - pent]
            else:
                next_p -= p[n - pent]
            i += 1
            if switch_sign:
                sign = not sign
            switch_sign = not switch_sign
        next_mod = next_p % div
        if not next_mod:
            return n
        p.append(next_mod)
        n += 1

if __name__ == '__main__':
    """ starts here """
    start = time.time()
    print(solve(1000000)) # 55374 
    print(time.time() - start) # 6.975 sec
