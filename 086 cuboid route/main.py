# A spider, S, sits in one corner of a cuboid room, 
# measuring 6 by 5 by 3, and a fly, F, sits in the opposite corner. 
# By travelling on the surfaces of the room the shortest 
# "straight line" distance from S to F is 10 and the path is shown 
# on the diagram.
# However, there are up to three "shortest" path candidates for any 
# given cuboid and the shortest route doesn't always have integer length.
# It can be shown that there are exactly 2060 distinct cuboids, 
# ignoring rotations, with integer dimensions, up to a 
# maximum size of M by M by M, for which the shortest route has 
# integer length when M = 100. This is the least value of M for 
# which the number of solutions first exceeds two thousand; 
# the number of solutions when M = 99 is 1975.
# Find the least value of M such that the number of solutions first 
# exceeds one million.
# Result: 

from typing import Callable, Generator, Set, List, Tuple, Dict
import time
import sys
import math

sys.path.append(".")
from util import babyl_sqrt
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

def has_integer_path(l, m, n) -> int:
    # Note this assumes l > m > n
    return 1 if babyl_sqrt(pow(l, 2) + pow(m + n, 2)) > 0 else 0

def solve_slow(cuboids: int) -> int:
    # This works, but is slow, takes like 1.5 hr for 1000000
    # For each rect with sides <= L, check if min path is integer length
    L = 1
    count = has_integer_path(L, L, L)
    while count < cuboids:
        L += 1
        for m in range(1, L + 1):
            for n in range(1, m + 1):
                count += has_integer_path(L, m, n)
    return L

def solve(cuboids: int) -> int:
    # For each integer path length, find how many rectangles have it
    path = 0
    # Keep track of how many rectangles with max side <= index have
    # an int path. Note values will be updated until the path value 
    # exceeds sqrt(5) of of that index.
    # path^2 = l^2 + (m + n)^2
    # The smallest l we could have updates for occurs when m and n 
    # are maximized, so
    # path^2 = l^2 + (l + l)^2
    # path^2 = 5*l^2
    # path = sqrt(5) * l
    counts = [0]
    sqrt_5 = pow(5, 0.5)
    while True:
        path += 1
        counts.append(0)
        path_sq = pow(path, 2)
        l_min = math.ceil(path / sqrt_5)
        for l in range(l_min, path):
            # for each longest edge, calc the sum of the remaining edges
            # The shortest path is sqrt(l^2 + (m + n)2) so 
            # (m + n) = sqrt(path^2 - l^2)
            # if (m + n) is a whole number, there are rectangles with this path
            m_and_n = babyl_sqrt(path_sq - pow(l, 2))
            if m_and_n > 0:
                # Note babyl_sqrt returns negative if 
                # it can't find a whole number root
                # How many ways can we add m and n to get m+n, where
                # l >= m >= n?
                counts[l] += max(m_and_n // 2 - max(m_and_n - l - 1, 0), 0)
        count = 0
        for i in range(l_min):
            # If we only check up to l_min, we know these values won't 
            # grow anymore and if we exceed the target count, 
            # that's the answer.
            count += counts[i]
            if count > cuboids:
                return i

if __name__ == '__main__':
    """ starts here """
    start = time.time()
    # Examples: 2000 -> 100 (100 is 2060), 1974 -> 99 (99 is 1975)
    print(solve(1000000)) # 1818
    print(time.time() - start) # 17.435 sec
