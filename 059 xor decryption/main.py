# Each character on a computer is assigned a unique code and the preferred 
# standard is ASCII (American Standard Code for Information Interchange). 
# For example, uppercase A = 65, asterisk (*) = 42, and lowercase k = 107.
# A modern encryption method is to take a text file, convert the bytes to 
# ASCII, then XOR each byte with a given value, taken from a secret key. 
# The advantage with the XOR function is that using the same encryption key 
# on the cipher text, restores the plain text; for example, 65 XOR 42 = 107, 
# then 107 XOR 42 = 65.
# For unbreakable encryption, the key is the same length as the plain text 
# message, and the key is made up of random bytes. The user would keep the 
# encrypted message and the encryption key in different locations, and 
# without both "halves", it is impossible to decrypt the message.
# Unfortunately, this method is impractical for most users, so the modified 
# method is to use a password as a key. If the password is shorter than 
# the message, which is likely, the key is repeated cyclically throughout 
# the message. The balance for this method is using a sufficiently long 
# password key for security, but short enough to be memorable.
# Your task has been made easy, as the encryption key consists of three 
# lower case characters. Using p059_cipher.txt 
# (right click and 'Save Link/Target As...'), a file containing the 
# encrypted ASCII codes, and the knowledge that the plain text must 
# contain common English words, decrypt the message and find the sum of 
# the ASCII values in the original text.
# Result: 129448

import math
from typing import Set, List, Tuple, Dict
import time
import sys
sys.path.append(".")
from util import permute_pick_n
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

def get_cipher() -> List[int]:
    with open(os.path.join(__location__, "p059_cipher.txt")) as f:
        result = [ int(c) for c in f.readline().strip().split(",") ]
    return result

def xor_encrypt(source: List[int], key: List[int]) -> List[int]:
    result = []
    key_index = 0
    key_length = len(key)
    for s in source:
        result.append(s ^ key[key_index])
        key_index = (key_index + 1) % key_length
    return result

def check_for_sublist(text: List[int], term: List[int]) -> bool:
    term_len = len(term)
    text_len = len(text)
    start = 0
    end = text_len - term_len
    while True:
        try:
            start = text.index(term[0], start, end)
        except ValueError:
            return False
        match = True
        for i in range(1, term_len):
            if text[start + i] != term[i]:
                match = False
                break
        if match:
            return True
        start += 1

def has_matches(source: List[int], words: List[List[int]], to_find: int):
    hits = 0
    strikes = 0
    out = len(words) - to_find + 1
    for word in words:
        if check_for_sublist(source, word):
            hits += 1
        else:
            strikes += 1
        if hits == to_find:
            return True
        if strikes == out:
            return False
    return False

def word_to_ints(word: str) -> List[int]:
    return [ ord(c) for c in word ]
    
if __name__ == '__main__':
    """starts here"""
    start = time.time()
    source = get_cipher()
    a = ord('a')
    AND = word_to_ints("and")
    THE = word_to_ints("the")
    FOR = word_to_ints("for")
    THAT = word_to_ints("that")
    HAVE = word_to_ints("have")
    letters = [ i + a for i in range(26)]
    for key in permute_pick_n(letters, 3):
        trial = xor_encrypt(source, key)
        if has_matches(trial, [AND, THE, FOR], 3):
            print("".join([ chr(n) for n in trial ]))
            break
    print("".join([ chr(n) for n in key ])) # exp
    print(sum(trial)) # 129448
    print(time.time() - start) # 3.349 sec
