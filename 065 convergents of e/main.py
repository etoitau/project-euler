# https://projecteuler.net/problem=65
# Find the sum of digits in the numerator of the 100th 
# convergent of the continued fraction for e.
# Result: 272

import math
from typing import Generator, Set, List, Tuple, Dict
import time
import sys
sys.path.append(".")
from util import Frac, digital_sum
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

def e_continued_fraction_notation() -> Generator[int, None, None]:
    """ Gives the abbreviated continued fraction 
    notation for euler's constant 
    """
    yield 2
    i = 1
    while True:
        yield 1
        yield 2 * i
        yield 1
        i += 1

def continued_fraction_term(notation: List[int]) -> Frac:
    """ Given a continued fraction notation as a finite list,
    return the fractional representation of that convergent
    """
    result = Frac(notation[-1])
    for i in range(len(notation) - 2, -1, -1):
        result.invert().add(Frac(notation[i]))
    return result.simplify()

def solve(nth: int) -> int:
    e = e_continued_fraction_notation()
    terms: List[int] = []
    for _ in range(nth):
        terms.append(next(e))
    return digital_sum(continued_fraction_term(terms).n)

if __name__ == '__main__':
    """ starts here """
    start = time.time()
    print(solve(100)) # 272
    print(time.time() - start) # 0.001 sec
