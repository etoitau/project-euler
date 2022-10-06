# In the 5 by 5 matrix below, the minimal path sum from the top left to the 
# bottom right, by only moving to the right and down, is indicated in 
# bold red and is equal to 2427.
# [
#     [131, 673, 234, 103, 18],
#     [201, 96, 342, 965, 150],
#     [630, 803, 746, 422, 111],
#     [537, 699, 497, 121, 956],
#     [805, 732, 524, 37, 331]
# ]
# Find the minimal path sum from the top left to the bottom right by 
# only moving right and down in matrix.txt 
# (right click and "Save Link/Target As..."), a 31K text file 
# containing an 80 by 80 matrix.
# Result: 427337

from cmath import inf
import math
from typing import Callable, Generator, Set, List, Tuple, Dict
import time
import sys
sys.path.append(".")
from util import int_array_to_int
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

def load_matrix() -> List[List[int]]:
    matrix: List[List[int]] = []
    with open(os.path.join(__location__, "p081_matrix.txt")) as f:
        for input in f:
            matrix.append([int(n) for n in input.split(",")])
    return matrix

def solve(matrix: List[List[int]]) -> int:
    x_size = len(matrix[0])
    y_size = len(matrix)
    # Save the minimal path to the end from any given point
    # if we work from the end toward the beginning, we can calculate
    # each point just by looking at the points to the right and below
    # which we've already solved.
    memo = matrix.copy()
    for row_index in range(y_size - 1, -1, -1):
        for col_index in range(x_size - 1, -1, -1): 
            if col_index < x_size - 1:
                # Has something to the right
                add_col = memo[row_index][col_index + 1]
                if row_index < y_size - 1:
                    # and has something below
                    memo[row_index][col_index] += min(add_col, memo[row_index + 1][col_index])
                else:
                    memo[row_index][col_index] += add_col
            elif row_index < y_size - 1:
                # Only has something below
                memo[row_index][col_index] += memo[row_index + 1][col_index]     
    return memo[0][0]

if __name__ == '__main__':
    """ starts here """
    start = time.time()
    m = load_matrix()
    sample = [
        [131, 673, 234, 103, 18],
        [201, 96, 342, 965, 150],
        [630, 803, 746, 422, 111],
        [537, 699, 497, 121, 956],
        [805, 732, 524, 37, 331]
    ] # should be 2427
    print(solve(m)) # 427337
    print(time.time() - start) # 0.005 sec
