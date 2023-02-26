# Comparing two numbers written in index form like 2^11 and 3^7 is not 
# difficult, as any calculator would confirm that 2^11 = 2048 < 3^7 = 2187.
# However, confirming that 632382^518061 > 519432^525806 would be much more 
# difficult, as both numbers contain over three million digits.
# Using base_exp.txt (right click and 'Save Link/Target As...'), a 22K 
# text file containing one thousand lines with a base/exponent pair on 
# each line, determine which line number has the greatest numerical value.
# NOTE: The first two lines in the file represent the numbers in the 
# example given above.
# Result: 709

from typing import Callable, Generator, Iterable, Set, List, Tuple, Dict
import time
import sys
import math
from collections import OrderedDict, defaultdict
from string import whitespace

sys.path.append(".")
from util import babyl_sqrt
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
    
def get_pairs() -> List[Tuple[int, int]]:
    ret = []
    with open(os.path.join(__location__, "p099_base_exp.txt")) as f:
        for line in f:
            parts = line.split(",")
            ret.append((int(parts[0]), int(parts[1].strip(whitespace))))
    return ret

def solve() -> int:
    # if a^b > c^d, then
    # log(a^b) > log(c^d), and
    # b * log(a) > d * log(c)
    # the last expression is much easier to evaluate
    max_line: int = 0
    max_val: float = 0
    pairs = get_pairs()
    for i in range(len(pairs)):
        val = pairs[i][1] * math.log(pairs[i][0])
        if val > max_val:
            max_line = i
            max_val = val
    # looks like they count lines starting at 1
    return max_line + 1


if __name__ == '__main__':
    """ starts here """
    start = time.time()
    print(solve()) # 709
    print(time.time() - start) # 0.002s
