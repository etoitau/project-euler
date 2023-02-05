# Each of the six faces on a cube has a different digit (0 to 9) 
# written on it; the same is done to a second cube. By placing the two 
# cubes side-by-side in different positions we can form a variety of 
# 2-digit numbers.
# For example, the square number 64 could be formed:
# [6] [4]
# In fact, by carefully choosing the digits on both cubes it is 
# possible to display all of the square numbers below one-hundred: 
# 01, 04, 09, 16, 25, 36, 49, 64, and 81.
# For example, one way this can be achieved is by placing 
# {0, 5, 6, 7, 8, 9} on one cube and {1, 2, 3, 4, 8, 9} on the other cube.
# However, for this problem we shall allow the 6 or 9 to be turned 
# upside-down so that an arrangement like {0, 5, 6, 7, 8, 9} and 
# {1, 2, 3, 4, 6, 7} allows for all nine square numbers to be displayed; 
# otherwise it would be impossible to obtain 09.
# In determining a distinct arrangement we are interested in the 
# digits on each cube, not the order.
# {1, 2, 3, 4, 5, 6} is equivalent to {3, 6, 4, 1, 2, 5}
# {1, 2, 3, 4, 5, 6} is distinct from {1, 2, 3, 4, 5, 9}
# But because we are allowing 6 and 9 to be reversed, the two distinct 
# sets in the last example both represent the extended set 
# {1, 2, 3, 4, 5, 6, 9} for the purpose of forming 2-digit numbers.
# How many distinct arrangements of the two cubes allow for all of the 
# square numbers to be displayed?
# Result: 1217

from typing import Callable, Generator, Set, List, Tuple, Dict
import time
import sys
import math
from collections import OrderedDict

sys.path.append(".")
from util import combinations_no_repeats
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

def get_cubes() -> List[Set[int]]:
    # side values can be 0-9, and 6 is distinct from 9
    values = [ i for i in range(10) ]
    # get each distinct possible cube as a set
    sets = [ set(combo) for combo in combinations_no_repeats(values, 6) ]
    # when we chaeck if a cube has a digit, we want 6 == 9
    # so if a cube has one, add the other
    for side_set in sets:
        if 6 in side_set:
            side_set.add(9)
        elif 9 in side_set:
            side_set.add(6)
    return sets

# the one or two digit square numbers
# express them as tuples for easy digit reference
squares = [
    (0, 1),
    (0, 4),
    (0, 9),
    (1, 6),
    (2, 5),
    (3, 6),
    (4, 9),
    (6, 4),
    (8, 1)
]

def solve() -> int:
    # how many cube combos work
    count = 0
    # get all distinct cubes
    cubes = get_cubes()
    # consider each distinct cube pair
    for i in range(len(cubes) - 1):
        for j in range(i + 1, len(cubes)):
            # test the pair against each square
            valid = True
            for square in squares:
                if not ((square[0] in cubes[i] and square[1] in cubes[j]) \
                    or (square[0] in cubes[j] and square[1] in cubes[i])):
                    valid = False
                    break
            if valid:
                count += 1
    return count


if __name__ == '__main__':
    """ starts here """
    
    start = time.time()
    print(solve()) # 1217
    print(time.time() - start) # 0.017
