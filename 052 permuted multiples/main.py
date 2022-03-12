# It can be seen that the number, 125874, and its double, 
# 251748, contain exactly the same digits, but in a different order.
# Find the smallest positive integer, x, such that 2x, 3x, 4x, 
# 5x, and 6x, contain the same digits.
# Result: 142857

from typing import Set, List, Tuple, Dict
import time
import sys
sys.path.append(".")
from util import int_to_int_array, is_permutation
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
    
if __name__ == '__main__':
    """starts here"""
    start = time.time()
    # first digit has to be 1 for number of digits to remain the same for x6
    # number's digits must have 7 permutations at least, so at least 4 digits
    base = 1000
    mults = [6, 5, 4, 3, 2]
    not_done = True
    while not_done:
        for rest in range(base):
            candidate = base + rest
            candidate_array = int_to_int_array(candidate)
            works = True
            for mult in mults:
                candidate_mult = candidate * mult
                if not is_permutation(candidate_array, int_to_int_array(candidate_mult)):
                    works = False
                    break
            if works:
                print(candidate) # 142857
                not_done = False
                break
        base *= 10

    print(time.time() - start) # 0.227 sec
