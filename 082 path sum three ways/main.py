# The minimal path sum in the 5 by 5 matrix below, by starting 
# in any cell in the left column and finishing in any cell in 
# the right column, and only moving up, down, and right, is 
# indicated in red and bold; the sum is equal to 994.
# [
#     [131, 673, 234, 103, 18],
#     [201, 96, 342, 965, 150],
#     [630, 803, 746, 422, 111],
#     [537, 699, 497, 121, 956],
#     [805, 732, 524, 37, 331]
# ]
# Find the minimal path sum from the left column to the right 
# column in matrix.txt (right click and "Save Link/Target As..."), 
# a 31K text file containing an 80 by 80 matrix.
# Result: 260324

from typing import Callable, Generator, Set, List, Tuple, Dict
import time
import sys
sys.path.append(".")
from util import dijkstra_min_path_length, Node
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

def load_matrix() -> List[List[int]]:
    matrix: List[List[int]] = []
    with open(os.path.join(__location__, "p082_matrix.txt")) as f:
        for input in f:
            matrix.append([int(n) for n in input.split(",")])
    return matrix

def solve(matrix: List[List[int]]) -> int:
    # make matrix of nodes, no conn yet, add all to set
    x_size = len(matrix[0])
    y_size = len(matrix)
    nodes: List[List[Node]] = [[-1 for _ in range(x_size)] for _ in range(y_size)]
    node_set: Set[Node] = set()
    for y in range(y_size):
        for x in range(x_size):
            node = Node(matrix[y][x])
            nodes[y][x] = node
            node_set.add(node)
    # connect nodes
    for y in range(y_size):
        for x in range(x_size):
            if y > 0:
                nodes[y][x].children.append(nodes[y - 1][x])
            if y < (y_size - 1):
                nodes[y][x].children.append(nodes[y + 1][x])
            if x < (x_size - 1):
                nodes[y][x].children.append(nodes[y][x + 1])
    # add a start node pointing to first row
    start = Node(0)
    start.children = [ nodes[y][0] for y in range(y_size) ]
    node_set.add(start)
    # add an end node from all last row
    end = Node(0)
    for node in [ nodes[y][-1] for y in range(y_size) ]:
        node.children.append(end)
    node_set.add(end)
    
    return dijkstra_min_path_length(node_set, start, end)

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
    ] # should be 994
    print(solve(m)) # 260324
    print(time.time() - start) # 0.145
