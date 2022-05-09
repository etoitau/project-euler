# Consider quadratic Diophantine equations of the form:
# x^2 – Dy^2 = 1
# For example, when D=13, the minimal solution in x is 
# 649^2 – 13×180^2 = 1.
# It can be assumed that there are no solutions in positive 
# integers when D is square.
# By finding minimal solutions in x for D = {2, 3, 5, 6, 7}, 
# we obtain the following:
# 3^2 – 2×2^2 = 1
# 2^2 – 3×1^2 = 1
# 9^2 – 5×4^2 = 1
# 5^2 – 6×2^2 = 1
# 8^2 – 7×3^2 = 1
# Hence, by considering minimal solutions in x for D ≤ 7, the 
# largest x is obtained when D=5.
# Find the value of D ≤ 1000 in minimal solutions of x for 
# which the largest value of x is obtained.
# Result: 661

import math
from typing import Generator, Set, List, Tuple, Dict
import time
import sys
sys.path.append(".")
from util import square_root_convergent_generator
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

def solve_slow(limit: int) -> int:
    """ A fairly naive solution. Even with some optimization 
    it's hopelessly slow past limit of approx 60 
    """
    squares: List[int] = [ n * n for n in range(math.ceil(math.sqrt(limit)) + 1) ]
    is_square: Set[int] = set(squares)
    result = 0
    max_x = 0
    for d in range(2, limit + 1):
        if d in is_square:
            continue
        y_i = 1
        x_i = 2
        while True:
            test = squares[x_i] - d * squares[y_i]
            if test < 1:
                x_i += 1
                if x_i == len(squares):
                    squares.append(x_i * x_i)
            elif test > 1:
                y_i += 1
            else:
                if x_i > max_x:
                    max_x = x_i
                    result = d
                break
    return result

def solve(limit: int) -> int:
    """ Using the fundamental solution to Pell's equation 
    via continued fractions
    https://en.wikipedia.org/wiki/Pell%27s_equation#Fundamental_solution_via_continued_fractions
    """
    result = 0
    max_x = 0
    for d in range(2, limit + 1):
        for f in square_root_convergent_generator(d):
            if f.n * f.n - d * f.d * f.d == 1:
                if f.n > max_x:
                    max_x = f.n
                    result = d
                break
    return result

if __name__ == '__main__':
    """ starts here """
    start = time.time()
    print(solve(1000)) # 661
    print(time.time() - start) # 0.052 sec
