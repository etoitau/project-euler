# You are given the following information, but you may prefer to do 
# some research for yourself.
# 1 Jan 1900 was a Monday.
# Thirty days has September,
# April, June and November.
# All the rest have thirty-one,
# Saving February alone,
# Which has twenty-eight, rain or shine.
# And on leap years, twenty-nine.
# A leap year occurs on any year evenly divisible by 4, 
# but not on a century unless it is divisible by 400.
# How many Sundays fell on the first of the month during the 
# twentieth century (1 Jan 1901 to 31 Dec 2000)?
# Result: 171

import math
from typing import Set, List, Tuple, Dict
from functools import reduce
import time
import sys
sys.path.append(".")
from util import Node

def is_leap_year(year: int) -> bool:
    return not year % 400 or (not year % 4 and year % 100)

def month_offset(month: int, year: int):
    thirty = {3, 5, 8, 10} # {4, 6, 9, 11} but counting from 0
    if month in thirty:
        return 2 # 30 % 7
    if month == 1:
        return 1 if is_leap_year(year) else 0
    return 3 # 31 % 7

if __name__ == '__main__':
    """starts here"""
    # check first of each month and count
    start = time.time()

    mo = 0 # jan
    yr = 1900
    d = 1 # monday, 0 is sunday
    count = 0
    while yr < 2001: #(1 Jan 1901 to 31 Dec 2000)
        if yr > 1900 and d == 0:
            count += 1
        d += month_offset(mo, yr)
        d %= 7
        mo += 1
        if mo == 12:
            mo = 0
            yr += 1
    print(count) # 171
    print(time.time() - start) # 0.001 sec
