# It turns out that 12 cm is the smallest length of wire that can be 
# bent to form an integer sided right angle triangle in exactly one 
# way, but there are many more examples.
# 12 cm: (3,4,5)
# 24 cm: (6,8,10)
# 30 cm: (5,12,13)
# 36 cm: (9,12,15)
# 40 cm: (8,15,17)
# 48 cm: (12,16,20)
# In contrast, some lengths of wire, like 20 cm, cannot be bent to 
# form an integer sided right angle triangle, and other lengths allow 
# more than one solution to be found; for example, using 120 cm it is 
# possible to form exactly three different integer sided right angle 
# triangles.
# 120 cm: (30,40,50), (20,48,52), (24,45,51)
# Given that L is the length of the wire, for how many values of 
# L ≤ 1,500,000 can exactly one integer sided right angle triangle be 
# formed?
# Result: 

import math
from typing import Callable, Generator, Set, List, Tuple, Dict
import time
import sys
sys.path.append(".")
from util import factorials, int_to_int_array
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

def solve(max_perimeter: int) -> int:
    return 0

def slow_solve(max_perimeter: int) -> int:
    # I think this works but it's too slow to solve the problem

    # how many perimeters up to and including max_perimeter have
    # exactly one right triangle of integer length sides
    count = 0
    for perimeter in range(12, max_perimeter + 1):
        p_count = 0
        half_perimeter = perimeter // 2
        # max s1 is where s2 is 1 and hyp is s1 + 1
        # perimeter = s1 + s1 + 1 + 1
        # perimeter = 2 * s1 + 2
        # s1 = perimeter / 2 - 1
        for s1 in range(4, half_perimeter):
            s1_sq = s1 * s1
            # s2 is less than s1 by defniition
            # also perimeter = s1 + s2 + hyp 
            # and hyp >= s1 + 1
            # perimeter = s1 + s1 + 1 + s2
            # s2 = perimeter - 2 * s1 - 1
            s2_max = min(s1, perimeter - (2 * s1) - 1)
            # also 
            # s1 + s2 > hyp
            # hyp = perimeter - s1 -s2
            # s1 + s2 > perimeter - s1 - s2
            # 2 s1 + 2 s2 > perimeter
            # s2 > perimeter / 2 - s1
            s2_min = max(3, half_perimeter - s1 + 1)
            for s2 in range(s2_min, s2_max + 1):
                hyp = perimeter - s1 - s2
                hyp_minus = hyp * hyp - s1_sq - (s2 * s2)
                if hyp_minus < 0:
                    # s2 has gotten too big
                    break
                if hyp_minus == 0:
                    # is right triangle
                    p_count += 1
                    break
            if p_count > 1:
                break
        if p_count == 1:
            count += 1
    return count

if __name__ == '__main__':
    """ starts here """
    start = time.time()
    print(solve(1500)) # 
    print(time.time() - start) #  sec
