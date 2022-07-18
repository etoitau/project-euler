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
# Result: 161667

import math
from typing import Callable, Generator, Set, List, Tuple, Dict
import time
import sys
sys.path.append(".")
from util import babyl_sqrt, primitive_pythagorean_triplets
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

def also_slow_solve(max_perimeter: int) -> int:
    """ how many perimeters up to and including max_perimeter have
    exactly one right triangle of integer length sides 
    """
    # I think this works but it's too slow to solve the problem
    # 100 sec for max_perimeter 15000
    p_count: Dict[int, int] = dict()
    half_perimeter = max_perimeter // 2
    for s1 in range(4, half_perimeter):
        s1_sq = s1 * s1
        # s2 is less than s1 by defniition
        # also perimeter = s1 + s2 + hyp 
        # and hyp >= s1 + 1
        # perimeter <= s1 + s1 + 1 + s2
        # s2 <= perimeter - 2 * s1 - 1
        s2_max = min(s1 - 1, max_perimeter - (2 * s1) - 1)
        for s2 in range(3, s2_max + 1):
            hyp_sq = s2 * s2 + s1_sq
            hyp = babyl_sqrt(hyp_sq)
            p = s1 + s2 + abs(hyp)
            if p > max_perimeter:
                break
            if hyp > 0:
                if p in p_count:
                    p_count[p] += 1
                else:
                    p_count[p] = 1
    count = 0
    for c in p_count.values():
        if c == 1:
            count += 1
    return count

def slow_solve(max_perimeter: int) -> int:
    """ how many perimeters up to and including max_perimeter have
    exactly one right triangle of integer length sides 
    """
    # I think this works but it's too slow to solve the problem
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

def solve(max_perimeter: int) -> int:
    """ how many perimeters up to and including max_perimeter have
    exactly one right triangle of integer length sides 
    """
    # a + b + c <= max_perimeter
    # 1 + c - 1 + c <= max_perimeter
    # c <= max_perimeter / 2
    # c = m^2 + n^2
    # max allowable m is when n is very small, so
    # max_perimeter / 2 = m^2 + 1
    # m = sqrt(max_perimeter / 2 - 1)
    m_limit = math.ceil(math.sqrt(max_perimeter / 2 - 1))
    count = [0] * (max_perimeter + 1)
    for primitive in primitive_pythagorean_triplets(m_limit):
        prim_p = sum(primitive)
        p = prim_p
        while p <= max_perimeter:
            count[p] += 1
            p += prim_p
    result = 0
    for c in count:
        if c == 1:
            result += 1
    return result

if __name__ == '__main__':
    """ starts here """
    start = time.time()
    print(solve(1500000)) # 161667
    print(time.time() - start) # 0.591 sec
