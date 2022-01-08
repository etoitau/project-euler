# A palindromic number reads the same both ways. The largest palindrome made 
# from the product of two 2-digit numbers is 9009 = 91 × 99.
# Find the largest palindrome made from the product of two 3-digit numbers.
# Result: 906609

import math
from typing import Set

def is_palindrome(n: int) -> bool:
    as_str = str(n)
    s = 0
    e = len(as_str) - 1
    while(s < e):
        if as_str[s] != as_str[e]:
            return False
        s += 1
        e -= 1
    return True

def largest_palindrome_product(min_limit: int, max_limit: int) -> int:
    max_pal = -1
    for a in range(max_limit - 1, min_limit, -1):
        if a * a < max_pal:
            break
        for b in range(a, min_limit, -1):
            prod = a * b
            if prod < max_pal:
                break
            if is_palindrome(prod):
                max_pal = prod
    return max_pal


if __name__ == '__main__':
    """starts here"""
    print(largest_palindrome_product(100, 1000))