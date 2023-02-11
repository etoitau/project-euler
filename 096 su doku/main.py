# Su Doku (Japanese meaning number place) is the name given to 
# a popular puzzle concept. Its origin is unclear, but credit 
# must be attributed to Leonhard Euler who invented a similar, 
# and much more difficult, puzzle idea called Latin Squares. 
# The objective of Su Doku puzzles, however, is to replace the 
# blanks (or zeros) in a 9 by 9 grid in such that each row, 
# column, and 3 by 3 box contains each of the digits 1 to 9. 
# Below is an example of a typical starting puzzle grid and its 
# solution grid.
# p096_1.png     p096_2.png
# A well constructed Su Doku puzzle has a unique solution and 
# can be solved by logic, although it may be necessary to employ 
# "guess and test" methods in order to eliminate options 
# (there is much contested opinion over this). The complexity of 
# the search determines the difficulty of the puzzle; the example 
# above is considered easy because it can be solved by straight 
# forward direct deduction.
# The 6K text file, sudoku.txt (right click and 'Save Link/Target As...'), 
# contains fifty different Su Doku puzzles ranging in difficulty, 
# but all with unique solutions (the first puzzle in the file is 
# the example above).
# By solving all fifty puzzles find the sum of the 3-digit numbers 
# found in the top left corner of each solution grid; 
# for example, 483 is the 3-digit number found in the top left 
# corner of the solution grid above.
# Result: 

from typing import Callable, Generator, Set, List, Tuple, Dict
import time
import sys
import math
from collections import OrderedDict

sys.path.append(".")
from util import combinations_in_order
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

class Cell:
    """ Represents a cell in a Sudoku board """

    def __init__(self, row: List['Cell'], col: List['Cell'], sqr: List['Cell']) -> None:
        # Add this cell to each of it's member groups
        # and keep a reference to those groups to update when set
        row.append(self)
        col.append(self)
        sqr.append(self)
        self.groups: List[List['Cell']] = [row, col, sqr]
        # Current value. 0 indicates unset
        self.val: int = 0
        # Remaining values this cell could take. Starts at 1-9
        self.pos: Set[int] = set([ i for i in range(1, 10)])

    def exclude(self, val: int) -> None:
        """ Specify that this cell cannot have the given value
        raises ValueError if this creates a contradiction.
        """
        if self.val:
            if self.val == val:
                raise ValueError
            return
        self.pos.discard(val)
        if not len(self.pos):
            # If cell has no remaining possible values, that's no good
            raise ValueError
        elif len(self.pos) == 1:
            # If one possibility remains, 
            # we can set this cell as that value 
            # (will raise ValueError if that creates a contradiction)
            self.set(self.pos.pop())

    def set(self, val: int) -> None:
        """ Assign this cell the given value 
        raises ValueError if that creates a contradiction.
        """
        if not val:
            return
        if self.val:
            if self.val == val:
                return
            else:
                raise ValueError
        self.val = val
        self.pos.clear()
        # Update this cell's peers to say they can't have
        # this value
        for group in self.groups:
            for cell in group:
                if cell is not self:
                    cell.exclude(val)

    def __str__(self) -> str:
        return str(self.val)

    def __repr__(self) -> str:
        return self.__str__()

class Board:
    """ Represents a Sudoku board """
    
    def __init__(self) -> None:
        # Create lists to organize our cells
        self.cells: List[Cell] = []
        self.rows: List[Cell] = [ [] for _ in range(9) ]
        self.cols: List[Cell] = [ [] for _ in range(9) ]
        self.sqrs: List[Cell] = [ [] for _ in range(9) ]
        self.first_unset = 0
        # Create the cells. They need a reference to the groups
        # they are members of, so they can try to update their 
        # peers when they become set
        for i in range(81):
            row = i // 9
            col = i % 9
            sqr = (row // 3) * 3 + col // 3
            self.cells.append(
                Cell(self.rows[row], self.cols[col], self.sqrs[sqr])
                )

    def copy(self) -> 'Board':
        """ Get a deep copy of this board """
        copy = Board()
        for i in range(81):
            copy.cells[i].set(self.cells[i].val)
        return copy

    def is_complete(self) -> bool:
        for cell in self.cells:
            if not cell.val:
                return False
        return True

    def next_unset(self) -> int:
        # Return the index in self.cells of the first unset cell
        # memoize the result so this is O(1) on average
        while self.first_unset < 81 and self.cells[self.first_unset].val:
            self.first_unset += 1
        if self.first_unset == 81:
            return None
        else:
            return self.first_unset

    def __str__(self) -> str:
        ret = str(self.cells[0])
        for i in range(1, 81):
            if not i % 9:
                ret += "\n"
            ret += str(self.cells[i])
        return ret

    def __repr__(self) -> str:
        return self.__str__()
        

def solve_board(input: List[List[int]]) -> Board:
    # create a board and populate with data
    board = Board()
    for i in range(81):
        board.cells[i].set(input[i // 9][i % 9])
    # it's possible the board is complete now 
    # based on simple elimination
    if board.is_complete():
        return board
    # if not, use the more powerful solver
    return dfs_solve(board)

def dfs_solve(board: Board) -> Board:
    # Assume each of the possible values for the next unset cell and 
    # recursively call until a violation is found or the board is complete

    # index of next unset cell
    i_next_cell = board.next_unset()
    if i_next_cell == None: 
        # if there is no unset cell
        if board.is_complete():
            return board
        else: 
            raise ValueError()
    for val in board.cells[i_next_cell].pos:
        # for each remaining value this cell could take
        # try it and see if it completes or encounters and error        
        board_copy = board.copy()
        try:
            board_copy.cells[i_next_cell].set(val)
            # that didn't raise an error, try the next unset cell
            board_copy = dfs_solve(board_copy)
        except ValueError:
            # that value's no good, try the next one
            continue
        return board_copy
    # None of the values were any good. This is a dead end.
    raise ValueError
    

def solve() -> int:
    count = 0
    with open(os.path.join(__location__, "p096_sudoku.txt")) as f:
        lines = f.readlines()
        for i in range(0, len(lines), 10):
            # data is in groups of ten rows, with first row title
            # collect 9 rows of numbers into array
            cell_values: List[List[int]] = []
            for j in range(1, 10):
                cell_values.append([ int(c) for c in lines[i + j].strip() ])
            board = solve_board(cell_values)
            # read the first three numbers as one three-digit number and add
            count += board.cells[0].val * 100 \
                + board.cells[1].val * 10 \
                + board.cells[2].val
    return count


if __name__ == '__main__':
    """ starts here """
    start = time.time()
    print(solve()) # 24702
    print(time.time() - start) # 1.20s
