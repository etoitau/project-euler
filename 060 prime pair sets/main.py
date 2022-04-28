# The primes 3, 7, 109, and 673, are quite remarkable. By taking any two 
# primes and concatenating them in any order the result will always be prime. 
# For example, taking 7 and 109, both 7109 and 1097 are prime. The sum of these 
# four primes, 792, represents the lowest sum for a set of four primes with 
# this property.
# Find the lowest sum for a set of five primes for which any two primes 
# concatenate to produce another prime.
# Result: 26033

import math
from typing import Set, List, Tuple, Dict
import time
import sys
sys.path.append(".")
from util import ConnectedNode, PrimeMachine, combinations_no_repeats, count_digits, is_clique
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

def is_concat_prime(a: int, b: int, pm: PrimeMachine) -> bool:
    return pm.is_prime(a * pow(10, count_digits(b)) + b) \
        and pm.is_prime(b * pow(10, count_digits(a)) + a)
    
if __name__ == '__main__':
    """starts here"""
    start = time.time()
    pm = PrimeMachine(9000)
    nodes: List[ConnectedNode] = []
    i = 0 
    result: int = 0
    debug_limit = 1200 # Prevent infinite loops
    set_size = 5
    while not result and i < debug_limit:
        i += 1
        p = pm.get(i)
        next = ConnectedNode(p)
        for node in nodes:
            if is_concat_prime(node.value, p, pm):
                next.connected.add(node)
                node.connected.add(next)
        nodes.append(next)
        if len(next.connected) < set_size - 1:
            # if not connected to at least set_size - 1, can't be part of 
            # a clique of set_size
            continue
        candidates = []
        for c in next.connected:
            if len(c.connected) >= set_size - 1:
                # if not connected to at least set_size - 1, can't be part of 
                # a clique of set_size
                candidates.append(c)
        if len(candidates) < set_size - 1:
            # if not enough candidates to form a clique of set_size
            continue
        for combo in combinations_no_repeats(candidates, set_size - 1):
            if is_clique(combo):
                clique_sum = sum([ n.value for n in combo ]) + next.value
                if result:
                    result = min(result, clique_sum)
                else:
                    result = clique_sum
    print(result) # 26033
    print(time.time() - start) # 11.645 sec
