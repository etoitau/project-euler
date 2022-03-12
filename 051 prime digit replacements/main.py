# By replacing the 1st digit of the 2-digit number *3, it turns 
# out that six of the nine possible values: 13, 23, 43, 53, 73, 
# and 83, are all prime.
# By replacing the 3rd and 4th digits of 56**3 with the same 
# digit, this 5-digit number is the first example having seven 
# primes among the ten generated numbers, yielding the family: 
# 56003, 56113, 56333, 56443, 56663, 56773, and 56993. 
# Consequently 56003, being the first member of this family, 
# is the smallest prime with this property.
# Find the smallest prime which, by replacing part of the number 
# (not necessarily adjacent digits) with the same digit, is 
# part of an eight prime value family.
# Result: 121313

from itertools import permutations
import math
from typing import Set, List, Tuple, Dict
from functools import reduce
import time
import sys
sys.path.append(".")
from util import PrimeMachine, int_array_to_int, int_to_int_array
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
    
if __name__ == '__main__':
    """starts here"""
    start = time.time()
    pm = PrimeMachine(160000)
    # 56003 is the first with 7, can start from there (index 5683)
    pi = 5683
    not_found = True
    while not_found:
        candidate = pm.get(pi)
        candidate_array = int_to_int_array(candidate)
        candidate_length = len(candidate_array)
        # find the 0s, 1s, or 2s
        # don't need to look for 3s or greater, because we want the first 
        # element in the family, and if the one with 3s is the first, 
        # then there can't be 8
        for look_for in range(3):
            # find indexes of digits to replace
            indexes = [ i for i in range(candidate_length) if candidate_array[i] == look_for ]
            sibling = candidate_array.copy()
            strikes = 0
            for sub_in in range(1, 10):
                for i in indexes:
                    sibling[i] = sub_in
                sib_as_number = int_array_to_int(sibling)
                if not pm.is_prime(sib_as_number) or sib_as_number == candidate:
                    strikes += 1
                    if strikes == 3:
                        # Not possible to make it to 8
                        break
            if strikes < 3:
                not_found = False
                print(candidate) # 121313
                break
        pi += 1
    print(time.time() - start) # 0.684 sec
