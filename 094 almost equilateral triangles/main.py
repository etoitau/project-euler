# It is easily proved that no equilateral triangle exists with integral 
# length sides and integral area. However, the almost equilateral 
# triangle 5-5-6 has an area of 12 square units.
# We shall define an almost equilateral triangle to be a triangle for 
# which two sides are equal and the third differs by no more than one unit.
# Find the sum of the perimeters of all almost equilateral triangles with 
# integral side lengths and area and whose perimeters do not exceed 
# one billion (1,000,000,000).
# Result: 518408346

from cmath import sqrt
from itertools import permutations
from tkinter import N
from typing import Callable, Generator, Set, List, Tuple, Dict
import time
import sys
import math

sys.path.append(".")
from util import primitive_pythagorean_triplets
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))


def solve(limit: int) -> int:
    total_p = 0
    # call the two equal sides a and the third b
    # consider b to be the base
    # a vertical line, h, splits it into two right triangles
    # the area of the triangle is b * h
    # h = sqrt(a^2 - (b/2)^2)
    # area = b * sqrt(a^2 - (b/2)^2)
    # area^2 = b^2 * (a^2 - (b/2)^2)
    # area^2 = (a * b)^2 - b^4 / 4
    # area is int, so area^2 is int
    # a and b are int, so (a * b)^2 is int
    # so b^4 / 4 has to be int
    # (b^2 / 2)^2 is int
    # b^2 has to be even
    # b has to be even
    # b / 2 is int
    # area is b * h, area and b are int
    # so h is int
    # a, b / 2, and h are all int, so they are a pythagorean triple
    # further, they must be primitive pythagorean triples,
    # because if they are a multiple of a primitive, then a and b
    # must either be equal or differ by more than 1
    # so check all the primitive pythagorean triples
    for b2, h, a in primitive_pythagorean_triplets():
        if (abs(a - 2 * b2)) == 1:
            # if a and b differ by 1, then almost equilateral
            # check perimeter is in limit
            p = a + a + b2 + b2
            if p > limit:
                break
            total_p += p
    return total_p

if __name__ == '__main__':
    """ starts here """
    start = time.time()
    # current solve is very slow. can speed up by only checking odd a
    # different approach, get all pythagorean triples and check ones where c - 2a = +-1
    # if py trip then base and ht are both int, so area is int
    limit = 1000000000
    print(solve(limit)) # 518408346
    print(time.time() - start) # 152.4
