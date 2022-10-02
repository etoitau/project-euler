# A common security method used for online banking is to 
# ask the user for three random characters from a passcode. 
# For example, if the passcode was 531278, they may ask 
# for the 2nd, 3rd, and 5th characters; the expected reply 
# would be: 317.
# The text file, keylog.txt, contains fifty successful 
# login attempts.
# Given that the three characters are always asked for 
# in order, analyse[sic] the file so as to determine the 
# shortest possible secret passcode of unknown length.
# Result: 73162890

import math
from typing import Callable, Generator, Set, List, Tuple, Dict
import time
import sys
sys.path.append(".")
from util import int_array_to_int, int_to_int_array
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

def get_logins() -> List[List[int]]:
    # Get each login as a list of ints
    # return a list of logins
    logins: List[List[int]] = []
    with open(os.path.join(__location__, "p079_keylog.txt")) as f:
        for input in f:
            logins.append(int_to_int_array(int(input)))
    return logins

def get_matrix() -> List[List[int]]:
    # initialize a 10x10 matrix of 0s
    return [[0 for _ in range(10)] for _ in range(10)]

def login_to_after(login: List[int]) -> List[int]:
    # Make an after table for just this one login
    after = get_matrix()
    for i in range(len(login)):
        for j in range(i + 1, len(login)):
            after[login[i]][login[j]] += 1
    return after

def login_to_before(login: List[int]) -> List[int]:
    # Make a before table for just this one login
    before = get_matrix()
    for i in range(len(login) - 1, -1, -1):
        for j in range(i - 1, -1, -1):
            before[login[i]][login[j]] += 1
    return before

def add_login(login_counts: List[List[int]], aggregate: List[List[int]]) -> None:
    # Update the aggregate table with the input for one login
    for i in range(10):
        for j in range(10):
            aggregate[i][j] = max(aggregate[i][j], login_counts[i][j]) 

def login_tables(logins: List[List[int]]) -> Tuple[List[List[int]], List[List[int]]]:
    # Build the after and before tables
    after = get_matrix()
    before = get_matrix()
    for login in logins:
        add_login(login_to_before(login), before)
        add_login(login_to_after(login), after)
    return after, before

def max_col(table: List[List[int]]):
    # Find the column which currently has the greatest sum in table
    # return -1 if the table is all 0s
    max = 0
    max_index = -1
    for col_index in range(len(table[0])):
        col_sum = sum([table[row_index][col_index] for row_index in range(len(table))])
        if col_sum > max:
            max = col_sum
            max_index = col_index
    return max_index

def decrement_col(table: List[List[int]], col: int) -> None:
    # Subtract 1 from each row of the given column, not going below 0
    for row in range(len(table)):
        if table[row][col]:
            table[row][col] -= 1

def solve(logins: List[List[int]]) -> int:
    # Build two tables, an after table and a before table
    # In the after table, after[m][n] will say how many of integer 
    # n must occur after m in the original number, according to 
    # our study of the guesses. For example, if we see a guess: [1, 3, 3],
    # then after[1][3] must be at least 2.
    # The before table works in the same but opposite way
    # Then if we look at the before column with the highest sum, that
    # tells us that that number must be at the start, because it is before
    # everything the most. Add that to the start, and decrement the tables
    # accordingly. Do similar for the after table to build up the numbers
    # at the end, and continue until before and after are all zeros.
    after, before = login_tables(logins)
    start = []
    end = []
    while True:
        # find max col from before
        before_col = max_col(before)
        if before_col != -1:
            # subtract it from before table
            decrement_col(before, before_col)
            # subtract it from after table for each previously in start list
            for row in start:
                if after[row][before_col]:
                    after[row][before_col] -= 1
            # add that to start list
            start.append(before_col)

        # find max col from after
        after_col = max_col(after)
        if after_col != -1:
            # subtract from after table
            decrement_col(after, after_col)
            # subtract it from after table for each previously in start list
            for row in end:
                if before[row][after_col]:
                    before[row][after_col] -= 1
            # add that to end list
            end.append(after_col)
        if after_col == -1 and before_col == -1:
            break
    end.reverse()
    return int_array_to_int(start + end)

if __name__ == '__main__':
    """ starts here """
    start = time.time()
    print(solve(get_logins())) # 73162890
    print(time.time() - start) # 0.004 sec
