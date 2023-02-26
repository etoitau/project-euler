# By replacing each of the letters in the word CARE with 1, 2, 9, 
# and 6 respectively, we form a square number: 1296 = 362. What is 
# remarkable is that, by using the same digital substitutions, the 
# anagram, RACE, also forms a square number: 9216 = 962. We shall 
# call CARE (and RACE) a square anagram word pair and specify further 
# that leading zeroes are not permitted, neither may a different letter 
# have the same digital value as another letter.
# Using words.txt (right click and 'Save Link/Target As...'), a 16K 
# text file containing nearly two-thousand common English words, find 
# all the square anagram word pairs (a palindromic word is NOT considered 
# to be an anagram of itself).
# What is the largest square number formed by any member of such a pair?
# NOTE: All anagrams formed must be contained in the given text file.
# Result: 18769

from typing import Callable, Generator, Iterable, Set, List, Tuple, Dict
import time
import sys
import math
from collections import OrderedDict, defaultdict
from string import whitespace

sys.path.append(".")
from util import babyl_sqrt, count_digits, int_to_int_array
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
    
def get_word_list() -> List[str]:
    with open(os.path.join(__location__, "p098_words.txt")) as f:
        return [ s.strip(whitespace + '"') for s in f.readline().split(",") ]

def itr_to_pattern(i: Iterable) -> str:
    """ Return a string representation of the input
    where the values of the elements don't matter, but the
    positions of any repeat elements are preserved.
    e.g. fall -> 0122, buff -> 0122, 4255 -> 0122
    """
    digis = dict()
    cur = 0
    pat = ""
    for d in i:
        if not d in digis:
            digis[d] = str(cur)
            cur += 1
        pat += digis[d]
    return pat

def int_to_pattern(n: int) -> str:
    return itr_to_pattern(int_to_int_array(n))

def word_to_pattern(w: str) -> str:
    return itr_to_pattern(w)

def get_scheme(word: str, n: int) -> Dict[str, int]:
    """ What dictionary translates the given word into the given int. 
    Assumes such a translation is possible
    """
    digits = int_to_int_array(n)
    scheme: Dict[str, int] = dict()
    for i in range(len(word)):
        scheme[word[i]] = digits[i]
    return scheme

def word_to_number(word: str, scheme: Dict[str, int]):
    """ Use the given dictionary to convert the given word into a number.
    Assumes the dictionary has all characters of the word
    """
    rev = reversed(word)
    rad = 1
    res = 0
    for c in rev:
        res += rad * scheme[c]
        rad *= 10
    return res

def check_scheme(word: str, scheme: Dict[str, int]) -> int:
    """ Does applying this scheme to this word result in a square? 
    Return square if so, 0 if not
    """
    if not scheme[word[0]]:
        # no good if the first digit is 0
        return 0
    test_sqr = word_to_number(word, scheme)
    if babyl_sqrt(test_sqr) > 0:
        return test_sqr
    return 0

def solve() -> int:
    # read in words
    words = get_word_list()
    # identify anagram groups
    ana_to_words: Dict[str, List[str]] = defaultdict(lambda: [])
    for w in words:
        sw = "".join(sorted(w))
        ana_to_words[sw].append(w)
    # want to remove groups with one member
    keys_to_rm = []
    # note longest anagram
    max_len = 0
    # cache a pattern for each word in a anagram
    word_to_pattern_dict = dict()
    for k in ana_to_words.keys():
        if len(ana_to_words[k]) < 2:
            keys_to_rm.append(k)
            continue
        if max_len < len(k):
            max_len = len(k)
        for w in ana_to_words[k]:
            word_to_pattern_dict[w] = word_to_pattern(w)
    for k in keys_to_rm:
        del ana_to_words[k]
    # generate squares up to max word length
    limit = pow(10, max_len)
    base = 4
    # keep track of what squares can be made with a pattern
    pattern_to_squares: Dict[str, List[int]] = defaultdict(lambda: [])
    while True:
        square = base * base
        if square > limit:
            break
        pattern = int_to_pattern(square)
        pattern_to_squares[pattern].append(square)
        base += 1
    # initialize result
    max_square = 16
    max_digits = 2
    for ana_key in ana_to_words.keys():
        if len(ana_key) < max_digits:
            # no words in this group can make a bigger square than 
            # what we already have 
            continue
        # get anagram group
        ana_words = ana_to_words[ana_key]
        for i in range(len(ana_words) - 1):
            # for each word in the group
            i_word = ana_words[i]
            # what squares can be made with it
            i_squares = pattern_to_squares[word_to_pattern(i_word)]
            for i_square in i_squares:
                # what scheme gives us this square for this word
                scheme = get_scheme(i_word, i_square)
                # what other words in the group work with this scheme?
                for j in range(i + 1, len(ana_words)):
                    j_word = ana_words[j]
                    j_square = check_scheme(j_word, scheme)
                    if j_square:
                        # this works! update max square
                        if max_square < i_square:
                            max_square = i_square
                            max_digits = count_digits(max_square)
                        if max_square < j_square:
                            max_square = j_square
                            max_digits = count_digits(max_square) 
    return max_square


if __name__ == '__main__':
    """ starts here """
    start = time.time()
    print(solve()) # 18769
    print(time.time() - start) # 0.19s
