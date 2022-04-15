# If we take 47, reverse and add, 47 + 74 = 121, which is palindromic.
# Not all numbers produce palindromes so quickly. For example,
# 349 + 943 = 1292,
# 1292 + 2921 = 4213
# 4213 + 3124 = 7337
# That is, 349 took three iterations to arrive at a palindrome.
# Although no one has proved it yet, it is thought that some numbers, 
# like 196, never produce a palindrome. A number that never forms a palindrome 
# through the reverse and add process is called a Lychrel number. 
# Due to the theoretical nature of these numbers, and for the purpose 
# of this problem, we shall assume that a number is Lychrel until proven 
# otherwise. In addition you are given that for every number below 
# ten-thousand, it will either (i) become a palindrome in less than 
# fifty iterations, or, (ii) no one, with all the computing power that exists, 
# has managed so far to map it to a palindrome. In fact, 10677 is the first 
# number to be shown to require over fifty iterations before producing a 
# palindrome: 4668731596684224866951378664 (53 iterations, 28-digits).
# Surprisingly, there are palindromic numbers that are themselves 
# Lychrel numbers; the first example is 4994.
# How many Lychrel numbers are there below ten-thousand?
# Result: 249

from typing import Set, List, Tuple, Dict
import time
import sys
sys.path.append(".")
from util import is_palindrome, int_to_int_array
import os
import math

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

def is_lychrel(n: int) -> bool:
    a = int_to_int_array(n)
    for i in range(50):
        l = len(a)
        for j in range(l):
            if j < l / 2:
                a[j] += a[l - 1 - j]
            else:
                a[j] = a[l - 1 - j]
        for j in range(l - 1):
            if a[j] > 9:
                a[j] -= 10
                a[j + 1] += 1
        if a[-1] > 9:
            a[-1] -= 10
            a.append(1)
        if is_palindrome(a):
            return False
    return True
    
if __name__ == '__main__':
    """starts here"""
    start = time.time()
    count = 0
    for n in range(10000):
        if is_lychrel(n):
            count += 1
    print(count) # 249
    print(time.time() - start) # 0.152 sec
