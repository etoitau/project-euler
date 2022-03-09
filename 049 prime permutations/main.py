# The arithmetic sequence, 1487, 4817, 8147, in which each of the 
# terms increases by 3330, is unusual in two ways: 
# (i) each of the three terms are prime, and, 
# (ii) each of the 4-digit numbers are permutations of one another.
# There are no arithmetic sequences made up of three 
# 1-, 2-, or 3-digit primes, exhibiting this property, but 
# there is one other 4-digit increasing sequence.
# What 12-digit number do you form by concatenating the three 
# terms in this sequence?
# Result: 296962999629

from itertools import permutations
import math
from typing import Set, List, Tuple, Dict
from functools import reduce
import time
import sys
sys.path.append(".")
from util import PrimeMachine, int_to_int_array, is_permutation
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
    
if __name__ == '__main__':
    """starts here"""
    start = time.time()
    # each number has to be four digits
    # diference between a and b is same as b and c
    # for each prime, a > 1000
    # for each prime, b > a
    # is b a permutation of a?
    # c = b + b - a 
    # is c: prime, < 10000, and a permutation of a?
    # first four digit prime is the 169th, 1009
    # last four digit prime is the 1229th, 9973
    pm = PrimeMachine()
    for n1 in range(168, 1227):
        p1 = pm.get(n1)
        p1_array = int_to_int_array(p1)
        for n2 in range(n1 + 1, 1226):
            p2 = pm.get(n2)
            p3 = p2 + p2 - p1
            if p3 >= 10000:
                break
            if not is_permutation(p1_array, int_to_int_array(p2)):
                continue
            if pm.is_prime(p3) and is_permutation(p1_array, int_to_int_array(p3)):
                # 148748178147 (known), and 296962999629
                print("{}{}{}".format(p1, p2, p3)) 
    print(time.time() - start) # 0.725 sec
