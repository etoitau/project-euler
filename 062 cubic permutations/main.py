# The cube, 41063625 (3453), can be permuted to produce two other cubes: 
# 56623104 (3843) and 66430125 (4053). 
# In fact, 41063625 is the smallest cube which has exactly three permutations 
# of its digits which are also cube.
# Find the smallest cube for which exactly five permutations of its digits 
# are cube.
# Result: 127035954683

import math
from typing import Set, List, Tuple, Dict
import time
import sys
sys.path.append(".")
from util import int_array_to_int, int_to_int_array, permute
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

def is_cube(n: int) -> bool:
    r: float = n**(1./3.)
    return r.is_integer()

def solve3(num: int) -> int:
    """ Solve the problem for a given exact number 
    of permutations which are also cubes 
    """
    # Like solve2 but checking is_cube directly 
    # each time instead of caching results
    # Works, but too slow
    n = 0
    debug = 500
    while not debug or n < debug:
        n += 1
        next = n * n * n
        next_array = int_to_int_array(next)
        found = set()
        for perm in permute(next_array):
            candidate = int_array_to_int(perm)
            if is_cube(candidate):
                found.add(candidate)
        if len(found) == num:
            return next

def solve2(perms: int) -> int:
    """ Solve the problem for a given exact number 
    of permutations which are also cubes 
    """
    # General approach: for each cube, check all
    # permutations and count how many are also cubes
    # Works, but too slow
    cube_set: Set[int] = set()
    cube_list: List[int] = []
    checked_set: Set[int] = set()
    n = 0
    debug = 500
    while not debug or n < debug:
        n += 1
        next = n * n * n
        if not next in cube_set:
            cube_set.add(next)
            cube_list.append(next)
        next_array = int_to_int_array(next)
        key = int_array_to_int(sorted(next_array))
        if key in checked_set:
            continue
        checked_set.add(key)
        found = set()
        m = n
        for perm in permute(next_array):
            candidate = int_array_to_int(perm)
            while candidate > cube_list[-1]:
                m += 1
                cube_list.append(m * m * m)
                cube_set.add(cube_list[-1])
            if candidate in cube_set:
                found.add(candidate)
            if len(found) > perms:
                break
        if len(found) == perms:
            return next

def solve(size: int) -> int:
    """ Solve the problem for a given exact number 
    of permutations which are also cubes 
    """
    n = 0
    # key is the cube with digits reverse sorted
    # value is [first cube, count of cube permutations]
    counts: Dict[int, List[int]] = dict()
    while True:
        n += 1
        t = n * n * n
        key = int_array_to_int(sorted(int_to_int_array(t), reverse=True))
        if key in counts:
            counts[key][1] += 1
            if counts[key][1] == size:
                return counts[key][0]
        else:
            counts[key] = [t, 1]
    
if __name__ == '__main__':
    """starts here"""
    start = time.time()
    print(solve(5)) # 127035954683
    print(time.time() - start) # 0.052 sec
