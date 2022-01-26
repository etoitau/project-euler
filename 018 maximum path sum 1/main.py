# By starting at the top of the triangle below and moving to adjacent 
# numbers on the row below, the maximum total from top to bottom is 23.
# 3
# 7 4
# 2 4 6
# 8 5 9 3
# That is, 3 + 7 + 4 + 9 = 23.
# Find the maximum total from top to bottom of the triangle below:
# 75
# 95 64
# 17 47 82
# 18 35 87 10
# 20 04 82 47 65
# 19 01 23 75 03 34
# 88 02 77 73 07 63 67
# 99 65 04 28 06 16 70 92
# 41 41 26 56 83 40 80 70 33
# 41 48 72 33 47 32 37 16 94 29
# 53 71 44 65 25 43 91 52 97 51 14
# 70 11 33 28 77 73 17 78 39 68 17 57
# 91 71 52 38 17 14 91 43 58 50 27 29 48
# 63 66 04 68 89 53 67 30 73 16 69 87 40 31
# 04 62 98 27 23 09 70 98 73 93 38 53 60 04 23
# NOTE: As there are only 16384 routes, it is possible to solve 
# this problem by trying every route. However, Problem 67, 
# is the same challenge with a triangle containing one-hundred rows; 
# it cannot be solved by brute force, and requires a clever method! ;o)
# Result: 1074

import math
from typing import Set, List, Tuple, Dict
from functools import reduce
import time
import sys
sys.path.append(".")
from util import Node


def triangle_to_graph(values: List[List[int]]) -> List[Node]:
    # Convert values to nodes
    nodes: List[List[Node]] = [ [] ]
    result: List[Node] = []
    for tier_index in range(len(values)):
        nodes.append([ Node(v) for v in values[tier_index] ])
        result.extend(nodes[tier_index])
    # Connect nodes
    for tier_index in range(len(nodes) - 1):
        for node_index in range(len(nodes[tier_index])):
            nodes[tier_index][node_index].children = [ 
                nodes[tier_index + 1][node_index], 
                nodes[tier_index + 1][node_index + 1] 
                ]
    return result

def string_to_ints(as_string: str) -> List[int]:
    return [ int(s) for s in as_string.split(" ") ]

def strings_to_graph(strings: List[str]) -> List[Node]:
    return triangle_to_graph([ string_to_ints(s) for s in strings ])

def max_value_trip(graph: List[Node]) -> int:
    # keep max downstream value from ea node
    memo: Dict[Node, int] = dict()
    return max_value_helper(graph[0], memo)

def max_value_helper(node: Node, memo: Dict[Node, int]) -> int:
    if not node:
        return 0
    if node in memo:
        return memo[node]
    child_max = 0
    for child in node.children:
        child_max = max(child_max, max_value_helper(child, memo))
    memo[node] = node.value + child_max
    return memo[node]

if __name__ == '__main__':
    """starts here"""
    # n = ["3",
    #     "7 4",
    #     "2 4 6",
    #     "8 5 9 3"]
    n = ["75",
        "95 64",
        "17 47 82",
        "18 35 87 10",
        "20 04 82 47 65",
        "19 01 23 75 03 34",
        "88 02 77 73 07 63 67",
        "99 65 04 28 06 16 70 92",
        "41 41 26 56 83 40 80 70 33",
        "41 48 72 33 47 32 37 16 94 29",
        "53 71 44 65 25 43 91 52 97 51 14",
        "70 11 33 28 77 73 17 78 39 68 17 57",
        "91 71 52 38 17 14 91 43 58 50 27 29 48",
        "63 66 04 68 89 53 67 30 73 16 69 87 40 31",
        "04 62 98 27 23 09 70 98 73 93 38 53 60 04 23"]
    start = time.time()
    print(max_value_trip(strings_to_graph(n))) # 1074
    print(time.time() - start) # 0.001 sec
