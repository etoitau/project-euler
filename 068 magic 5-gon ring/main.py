# Consider the following "magic" 3-gon ring, filled with the 
# numbers 1 to 6, and each line adding to nine.
#     4
#      \
#       3
#      / \
#     1 - 2 - 6
#    /
#   5
# Working clockwise, and starting from the group of three 
# with the numerically lowest external node 
# (4,3,2 in this example), each solution can be described 
# uniquely. For example, the above solution can be described 
# by the set: 4,3,2; 6,2,1; 5,1,3.
# It is possible to complete the ring with four different 
# totals: 9, 10, 11, and 12. 
# There are eight solutions in total.
# Total	Solution Set
# 9     4,2,3; 5,3,1; 6,1,2
# 9     4,3,2; 6,2,1; 5,1,3
# 10    2,3,5; 4,5,1; 6,1,3
# 10    2,5,3; 6,3,1; 4,1,5
# 11    1,4,6; 3,6,2; 5,2,4
# 11    1,6,4; 5,4,2; 3,2,6
# 12    1,5,6; 2,6,4; 3,4,5
# 12    1,6,5; 3,5,4; 2,4,6
# By concatenating each group it is possible to form 
# 9-digit strings; the maximum string for a 3-gon ring 
# is 432621513.
# Using the numbers 1 to 10, and depending on arrangements, 
# it is possible to form 16- and 17-digit strings. 
# What is the maximum 16-digit string for a "magic" 5-gon ring?
# Result: 6531031914842725

import math
from typing import Generator, Set, List, Tuple, Dict
import time
import sys
sys.path.append(".")
from util import Node
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

class Ring:
    def __init__(self, nodes: List[int] = None) -> None:
        self.target = 0
        # self.nodes is 15 ints, the values in each group of three, working
        # clockwise around the ring, and from tip to pentagon corner
        self.nodes = [ n for n in nodes ]
        if len(self.nodes) > 2:
            self.target = self.nodes[0] + self.nodes[1] + self.nodes[2]
        
    def can_add(self, n: int) -> bool:
        """ Does n work as the next value in the ring? """
        i = len(self.nodes)
        
        # The first three are unconstrained
        if i < 3:
            return True
        
        if not i % 3:
            # Adding to the first in the group of three, on the outer edge.
            # This is only constrained if it's the last one
            if i != 12:
                return True
            if (n + self.nodes[11] + self.nodes[1]) == self.target:
                return True
            return False
        
        # It should never be the second in the group of three, 
        # because the in that position is the same as the third 
        # node in the previous group of three so it gets added automatically

        # If third in the group of three, needs to add to target with the other two
        if (n + self.nodes[i - 1] + self.nodes[i - 2]) == self.target:
            return True
        return False

    def add(self, n: int) -> None:
        i = len(self.nodes)
        self.nodes.append(n)
        if i == 2:
            self.target = self.nodes[0] + self.nodes[1] + self.nodes[2]
        if i >= 3 and not i % 3:
            # The next node is the same as the last in the previous group
            # Go ahead and add it
            self.nodes.append(self.nodes[i - 1])
            # If this is the last group, we also know the last of the three
            # because it's the second in the first group.
            if i == 12:
                self.nodes.append(self.nodes[1])
        return

    def get_value(self) -> int:
        # find min in outer ring
        min_i = 3
        for i in range(6, 15, 3):
            if self.nodes[i] < self.nodes[min_i]:
                min_i = i
        # assemble from there
        ordered = []
        for i in range(15):
            ordered.append(self.nodes[(min_i + i) % 15])
        return int("".join([ str(n) for n in ordered ]))    
 
def solve() -> int:
    # We know the 10 has to be on the outer edge, because otherwise it will
    # show up twice in the result and give a number with 17 digits 
    # instead of 16. So let's call that our starting point.
    start = Ring([10])
    to_add: Set[int] = set(range(9, 0, -1))
    full_rings: List[Ring] = []
    recur(start, to_add, full_rings)
    max_solution = full_rings[0].get_value()
    for i in range(1, len(full_rings)):
        value = full_rings[i].get_value()
        if value > max_solution:
            max_solution = value
    return max_solution

def recur(start: Ring, to_add: Set[int], full_rings: List[Ring]) -> None:
    if not len(to_add):
        full_rings.append(start)
        return
    for n in to_add:
        if start.can_add(n):
            new_ring = Ring(start.nodes)
            new_ring.add(n)
            copy = set(to_add)
            copy.remove(n)
            recur(new_ring, copy, full_rings)
    return    

if __name__ == '__main__':
    """ starts here """
    start = time.time()
    print(solve()) # 6531031914842725
    print(time.time() - start) # 0.012 sec
