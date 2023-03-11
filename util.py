import math
import sys
from typing import Callable, Dict, Generator, Iterable, Set, List, Tuple, TypeVar
from functools import reduce
import time

T = TypeVar("T")

class NodeBase:
    def __init__(self, value) -> None:
        self.value = value

    def __str__(self) -> str:
        return str(self.value)
    
    def __repr__(self) -> str:
        return repr(self.value)

class Node(NodeBase):
    def __init__(self, value) -> None:
        super(Node, self).__init__(value)
        self.children: List['Node'] = []

    def report(self) -> str:
        return (str(self.value) + "->[" 
            + ", ".join([ str(c.value) for c in self.children ]) 
            + "]")

class ConnectedNode(NodeBase):
    def __init__(self, value) -> None:
        super(ConnectedNode, self).__init__(value)
        self.connected: Set['ConnectedNode'] = set()

    def report(self) -> str:
        return (str(self.value) + "->[" 
            + ", ".join([ str(c.value) for c in self.connected ]) 
            + "]")

def is_clique(nodes: List[ConnectedNode]):
    for i in range(len(nodes) - 1):
        for j in range(i + 1, len(nodes)):
            if nodes[j] not in nodes[i].connected:
                return False
    return True


class Heap:
    ''' A min or max heap, depending on the comparison function provided.
    A typical function where if a < b cmp(a, b) < 0 will give a min heap.
    '''
    def __init__(self, cmp: Callable[[T, T], float], elements: Iterable[T]):
        self.cmp = cmp
        self.elements = list(elements) if elements else []
        self.element_to_index: Dict[T, int] = dict()
        self.heapify()

    def priority(self, a: int, b: int) -> bool:
        # should a be above b in the heap?
        return self.cmp(self.elements[a], self.elements[b]) < 0

    def heapify(self):
        # start at bottom of tree and work up, sifting 
        # everything down, except leaves can be skipped
        for i in range((len(self.elements) - 2) // 2, -1, -1):
            self.sift_down(i)
        for i in range(len(self.elements)):
            self.element_to_index[self.elements[i]] = i

    def index_of(self, element: T) -> int:
        return self.element_to_index[element]

    def left(self, i: int) -> int:
        return 2 * i + 1

    def right(self, i: int) -> int:
        return 2 * i + 2

    def parent(self, i: int) -> int:
        return (i - 1) // 2

    def swap(self, i: int, j: int) -> None:
        self.elements[i], self.elements[j] = self.elements[j], self.elements[i]
        self.element_to_index[self.elements[i]] = i
        self.element_to_index[self.elements[j]] = j

    def sift_down(self, i):
        # swap the element at i down through data until it's a 
        # leaf or smaller than both below
        max_index = i
        l = self.left(i)
        r = l + 1
        if l < len(self.elements) and self.priority(l, max_index):
            max_index = l
        if r < len(self.elements) and self.priority(r, max_index):
            max_index = r
        if i != max_index:
            self.swap(max_index, i)
            self.sift_down(max_index)

    def sift_up(self, i):
        if not i:
            return
        parent = self.parent(i)
        if self.priority(i, parent):
            self.swap(i, parent)
            self.sift_up(parent)

    def add(self, element: T):
        self.elements.append(element)
        self.element_to_index[element] = len(self.elements) - 1
        self.sift_up(len(self.elements) - 1)

    def get_root(self) -> T:
        # Get but don't remove the element at the root
        if not len(self.elements):
            return None
        return self.elements[0]

    def pop_root(self) -> T:
        # Get and remove the element at the root
        ret = self.get_root()
        if not ret:
            return None
        self.element_to_index.pop(ret)
        if len(self.elements) == 1:
            # that was last element
            self.elements.pop()
            return ret
        # move the last element to the root, then sift down
        last_elem = self.elements[-1]
        self.elements[0] = last_elem
        self.element_to_index[last_elem] = 0
        self.elements.pop() # shorten the array by 1
        self.sift_down(0)
        return ret

    def update(self, element: T):
        # Call to let the heap know the value of element has changed
        if element not in self.element_to_index:
            return
        i = self.element_to_index[element]
        p = self.parent(i)
        l = self.left(i)
        r = self.right(i)
        if i and self.priority(i, p):
            self.sift_up(i)
        elif (l < len(self.elements) and self.priority(l, i)) \
                or (r < len(self.elements)) and self.priority(r, i):
            self.sift_down(i)

class PrimeMachine:
    def __init__(self, initial_max=2048) -> None:
        self.up_to = max(10, min(initial_max, 500000))
        self.prime_list = prime_sieve(self.up_to)
        self.prime_set = set(self.prime_list)

    def __iter__(self):
        return PrimeIterator(self)

    def get(self, nth: int) -> int:
        if nth >= len(self.prime_list):
            for i in range(1 + nth - len(self.prime_list)):
                self.get_next()
        return self.prime_list[nth]
    
    def _get_more(self) -> None:
        i = len(self.prime_list)
        self.up_to <<= 1
        self.prime_list = prime_sieve(self.up_to, self.prime_list)
        self.prime_set.update(self.prime_list[i:])

    def get_next(self) -> None:
        current = self.up_to + 1
        if not current % 2:
            current += 1
        max_factor = math.sqrt(current)
        while True:
            is_prime = True
            for p in self.prime_list:
                if p > max_factor:
                    break
                if not current % p:
                    is_prime = False
                    break
            if is_prime:
                self.prime_list.append(current)
                self.prime_set.add(current)
                self.up_to = current
                return current
            else:
                current += 2
                max_factor = math.sqrt(current)

    def is_prime(self, n: int) -> bool:
        if n > self.up_to:
            return self.miller_test(n)
        return n in self.prime_set

    def prime_factors(self, n: int) -> Dict[int, int]:
        pf = prime_factors(n, self.prime_set)
        if 1 in pf:
            del pf[1]
        self.prime_set.update(pf.keys())
        return pf

    def miller_test(self, n: int) -> bool:
        # https://en.wikipedia.org/wiki/Miller%E2%80%93Rabin_primality_test#Deterministic_variants
        if n <= 1: 
            return False
        if n == 2:
            return True
        if not (n & 1):
            return False
        if n in self.prime_set:
            return True
        # n written as 2^r * d + 1
        d = n - 1
        r = 0
        while not (d & 1):
            r += 1
            d >>= 1
        for a in PrimeMachine.get_miller_a(n):
            x = pow(a, d, n)
            if x == 1 or x == (n - 1):
                continue
            maybe_prime = False
            for i in range(r - 1):
                x = pow(x, 2, n)
                if x == (n - 1):
                    maybe_prime = True
                    break
            if not maybe_prime:
                return False
        self.prime_set.add(n)
        return True
    
    @staticmethod
    def get_miller_a(n: int) -> List[int]:
        # https://en.wikipedia.org/wiki/Miller%E2%80%93Rabin_primality_test#Deterministic_variants
        if n < 2047:
            return [2]
        if n < 1373653:
            return [2, 3]
        if n < 9080191:
            return [31, 73]
        if n < 25326001:
            return [2, 3, 5]
        return [ 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37 ]

class PrimeIterator:
    def __init__(self, prime_machine=None):
        if prime_machine:
            self.machine = prime_machine
        else:
            self.machine = PrimeMachine()
        self.index = -1
    
    def __next__(self):
        self.index += 1
        return self.machine.get(self.index)

class Factorial:
    def __init__(self, facts: List[int] = None) -> None:
        self.facts = facts if facts else [ 1 ]
    
    def get(self, nth: int) -> int:
        while len(self.facts) <= nth:
            self.get_next()
        return self.facts[nth]
    
    def get_next(self) -> int:
        self.facts.append(self.facts[-1] * len(self.facts))
        return self.facts[-1]

class Frac:
    """ Representing a fraction - a numerator 'n' and demoninator 'd' """

    def __init__(self, n: int, d: int = 1) -> None:
        self.n = n
        self.d = d

    def simplify(self) -> 'Frac':
        self.n, self.d = simplify_fraction(self.n, self.d)
        return self
    
    def copy(self) -> 'Frac':
        return Frac(self.n, self.d)
    
    def multiply(self, f: 'Frac', simplify: bool = False) -> 'Frac':
        self.n *= f.n
        self.d *= f.d
        if simplify:
            self.simplify()
        return self

    def divide(self, f: 'Frac', simplify: bool = False) -> 'Frac':
        return self.multiply(Frac(f.d, f.n), simplify)
    
    def add(self, f: 'Frac', simplify: bool = False) -> 'Frac':
        prev_d = self.d
        self.d = lcm(self.d, f.d)
        self.n = (self.d // prev_d) * self.n + (self.d // f.d) * f.n
        if simplify:
            self.simplify()
        return self

    def subtract(self, f: 'Frac', simplify: bool = False) -> 'Frac':
        return self.add(Frac(-1).multiply(f), simplify)

    def invert(self) -> 'Frac':
        self.n, self.d = self.d, self.n
        return self

    def compare(self, other: 'Frac') -> int:
        """ Return int < 0 if self < other, int > 0 if self > other """
        return frac_subtract(self, other).n

    def get_float(self) -> float:
        return self.n / self.d

    def __str__(self) -> str:
        return "{}/{}".format(self.n, self.d)
    
    def __repr__(self) -> str:
        return str(self)

class GeneralizedPentagonalMachine:
    """ Used for getting generalized pentagonal numbers
    p(n) = n * (3 * n - 1) / 2
    where n goes like 0, 1, -1, 2, -2, 3, -3...
    """
    # My approach is to treat it like two series zipped together:
    # The normal positive pentagonals and the negative pentagonals
    # For each, the difference between successive elements increases
    # by three with each term 
    def __init__(self):
        self.pos = False
        self.pos_diff = 4
        self.neg_diff = 2
        self.pents = [0, 1]

    def get(self, nth: int) -> int:
        while len(self.pents) <= nth:
            self.get_next()
        return self.pents[nth]

    def get_next(self) -> int:
        if self.pos:
            p = self.pents[-2] + self.pos_diff
            self.pos_diff += 3
        else:
            p = self.pents[-2] + self.neg_diff
            self.neg_diff += 3
        self.pos = not self.pos
        self.pents.append(p)
        return p

def frac_multiply(f1: Frac, f2: Frac, simplify: bool = False) -> Frac:
    return f1.copy().multiply(f2, simplify)

def frac_divide(f1: Frac, f2: Frac, simplify: bool = False) -> Frac:
    return f1.copy().divide(f2, simplify)

def frac_add(f1: Frac, f2: Frac, simplify: bool = False) -> Frac:
    return f1.copy().add(f2, simplify)

def frac_subtract(f1: Frac, f2: Frac, simplify: bool = False) -> Frac:
    return f1.copy().subtract(f2, simplify)

def frac_invert(f: Frac) -> Frac:
    return Frac(f.d, f.n)

def simplify_fraction(n: int, d: int) -> Tuple[int, int]:
    r = gcd(n, d)
    return n // r, d // r

def gcd(a: int, b: int) -> int:
    """Greatest common denominator by Euler method"""
    while b:
        a, b = b, a % b
    return a 

def lcm(a: int, b: int) -> int:
    """Least common multiple"""
    return abs(a * b) // gcd(a, b)

def prime_sieve(n: int, primes: List[int]=[]) -> List[int]:
    """Get list of all primes less than or equal to n using Sieve of Eratosthenes
    Can optionally provide already calculated primes. 
    These should not be missing any in their range
    """
    sieve_start = 2
    is_prime = [True for i in range(n + 1)]
    if len(primes):
        if primes[-1] >= n:
            return primes
        sieve_start = primes[-1] + 1
        for i in range(primes[-1]):
            is_prime[i] = False
        for p in primes:
            is_prime[p] = True
            start = p ** 2
            if sieve_start > start:
                # Want to start at unknown #s, but need to start on mult of p
                start = sieve_start - (sieve_start % p)
            for i in range(start, n + 1, p):
                is_prime[i] = False
    c = sieve_start
    limit = math.sqrt(n)
    while (c <= limit):
        if (is_prime[c] == True):
            for i in range(c ** 2, n + 1, c):
                is_prime[i] = False
        c += 1
    is_prime[0]= False
    is_prime[1]= False
    for i in range(sieve_start, len(is_prime)):
        if is_prime[i]:
            primes.append(i)
    return primes

def nth_prime(n) -> int:
    """Return the nth prime number"""
    # Per prime number theorem, estimate upper bound
    upper_bound = 13 if n < 7 else round(n * (math.log(n) + math.log(math.log(n))) + 1)
    primes = prime_sieve(upper_bound)
    while len(primes) < n:
        # Look further if necessary (it shouldn't be)
        upper_bound = round(upper_bound * 1.5)
        primes = prime_sieve(upper_bound, primes)
    return primes[n - 1]

def prime_factors(n: int, known_primes: Set[int]=None) -> Dict[int, int]:
    """Get the prime factorization of the input. The result takes the form 
    of a dict where the keys are the primes and the values are how many times
    that prime occurs in the factorization.
    """
    if not known_primes:
        known_primes = set([1])
    factors = dict([(1, 1)])
    primes_helper(n, factors, known_primes)
    return factors

def primes_helper(n, factors: Dict[int, int], known_primes: Set[int]) -> None:
    """Recursive helper to do factorization by the tree method"""
    if n in factors:
        factors[n] += 1
        return
    elif n in known_primes:
        factors[n] = 1
    d = math.floor(math.sqrt(n))
    while d > 1:
        if not n % d:
            primes_helper(d, factors, known_primes)
            primes_helper(int(n / d), factors, known_primes)
            return
        d -= 1
    factors[n] = 1

def recombine(factors: Dict[int, int]) -> int:
    """Take a factorization of the form produced by prime_factors and put
    back together into the original number.
    """
    result = 1
    for f in factors:
        result *= int(math.pow(f, factors[f]))
    return result

def factors_to_divisors(factors: Dict[int, int]) -> List[int]:
    """Given a factorization of a number, n, of the form provided by prime_factors,
    return a list of all proper divisors of n by evaluating every possible factor product
    """
    ret = [ 1 ]
    # just primes without exponents, and leave out 1
    factor_list = list(filter(lambda a: a != 1, list(factors)))
    n_factors = len(factor_list)
    if not n_factors:
        return []
    current_exp = [0] * n_factors
    def one_prod() -> int:
        return reduce(
            lambda a, b: a * b, 
            [ factor_list[i] ** current_exp[i] for i in range(n_factors) ], 
            1)
    # iterate over all possible combinations of exponents
    while True:
        # inc first exp
        curr_digit = 0
        current_exp[curr_digit] += 1
        # do carrys as needed
        while current_exp[curr_digit] > factors[factor_list[curr_digit]]:
            current_exp[curr_digit] = 0
            curr_digit += 1
            # if we're trying to inc beyond max, then we're done
            if curr_digit == n_factors:
                # for proper divisors, leave off the last one, which was n
                return ret[:-1]
            current_exp[curr_digit] += 1
        # get this divisor
        ret.append(one_prod())

def totient(n: int, pm: PrimeMachine=None) -> int:
    """ How many integers between 0 and n are relatively prime to n? """
    # https://en.wikipedia.org/wiki/Euler's_totient_function#Computing_Euler's_totient_function
    if not pm:
        pm = PrimeMachine(math.ceil(math.sqrt(n)))
    factors = pm.prime_factors(n)
    result = n
    for prime in factors:
        # multiplying by (1 - 1/p) is equivalent to subtracting self / p
        result -= result // prime
    return result

def nth_ngonal(nth: int, ngon: int):
    return [
        lambda n: 0,
        lambda n: 1,
        lambda n: n,
        triangle_number,
        lambda n: n * n,
        pentagonal_number,
        hexagonal_number,
        heptagonal_number,
        octagonal_number
    ][ngon](nth)

def ngonal_inverse(num: int, ngon: int) -> float:
    def _raise(ex):
        raise ex
    return [
        lambda n: _raise(ValueError),
        lambda n: _raise(ValueError),
        lambda n: n,
        triangle_inverse,
        lambda n: math.sqrt(n),
        pentagonal_inverse,
        hexagonal_inverse,
        heptagonal_inverse,
        octagonal_inverse
    ][ngon](num)

def triangle_number(nth: int) -> int:
    return nth * (nth + 1) // 2

def triangles(n, known: List[int]=[ 0, 1 ]) -> List[int]:
    if n <= len(known) - 1:
        return known
    count = len(known) - 1
    value = known[count]
    while count < n:
        count += 1
        value += count
        known.append(value)
    return known

def triangle_inverse(t: int) -> float:
    return -.5 + math.sqrt(0.25 + 2 * t)

def which_triangle_number(t: int) -> int:
    n = triangle_inverse(t)
    if not n.is_integer():
        raise ValueError
    return int(n)

def is_triangle_number(n: int) -> bool:
    try:
        which_triangle_number(n)
        return True
    except ValueError:
        return False

def pentagonal_number(n: int) -> int:
    return int(n * (3 * n - 1) / 2)

def pentagonal_inverse(p: int) -> float:
    return (1 + math.sqrt(1 + 24 * p)) / 6

def which_pentagonal_number(p: int) -> int:
    n = pentagonal_inverse(p)
    if not n.is_integer():
        raise ValueError
    return int(n)

def is_pentagonal_number(n) -> bool:
    if not isinstance(n, (int, float)):
        return False
    if isinstance(n, float):
        if n.is_integer():
            n = int(n)
        else:
            return False
    try:
        which_pentagonal_number(n)
        return True
    except ValueError:
        return False

def hexagonal_number(n: int) -> int:
    return n * (2 * n - 1)

def hexagonal_inverse(h: int) -> float:
    return (1 + math.sqrt(1 + 8 * h)) / 4

def which_hexagonal_number(h: int) -> int:
    n = hexagonal_inverse(h)
    if not n.is_integer():
        raise ValueError
    return int(n)

def is_hexagonal_number(n) -> bool:
    if not isinstance(n, (int, float)):
        return False
    if isinstance(n, float):
        if n.is_integer():
            n = int(n)
        else:
            return False
    try:
        which_hexagonal_number(n)
        return True
    except ValueError:
        return False

def heptagonal_number(nth: int) -> int:
    return int(nth * (5 * nth - 3) / 2)

def heptagonal_inverse(h: int) -> float:
    return 0.3 + math.sqrt(2.25 + 10 * h) / 5

def octagonal_number(nth: int) -> int:
    return nth * (3 * nth - 2)

def octagonal_inverse(o: int) -> float:
    return (2 + math.sqrt(4 + 12 * o)) / 6

def radix_sort(to_sort: List[List[int]], as_number=True) -> None:
    """Sort to_sort in place
    if as_number is True, [4] will come before [1, 2] (i.e. 4 is less than 12)
    if as_number is False, sort like alphabetical (i.e. "12" is less than "4")
    """
    max_len = max(len(data) for data in to_sort)
    if as_number:
        for i in range(max_len):
            # sort digit by digit starting at last digit of each entry
            radix_helper(to_sort, (i + 1) * -1)
    else:
        for i in range(max_len):
            # sort digit by digit starting from last digit of longest entry
            radix_helper(to_sort, max_len - 1 - i)

def radix_helper(to_sort: List[List[int]], index: int) -> None:
    # Do counting sort on data sorting on the data in index
    
    # want min value to correspond to index 1 in our count array, 
    # with index 0 used by no value
    min_value = float('inf')
    max_value = float('-inf')
    for data in to_sort:
        try:
            max_value = max(max_value, data[index])
            min_value = min(min_value, data[index])
        except IndexError:
            pass
    offset = int(0 - min_value + 1)
    # Collect frequency of each value
    frequency = [0] * (2 + int(max_value - min_value))
    for data in to_sort:
        try:
            frequency[data[index] + offset] += 1
        except IndexError:
            frequency[0] += 1
    # Accumulate
    for i in range(1, len(frequency)):
        frequency[i] += frequency[i - 1]
    # Offset by 1 so value at frequency[value + offset] tells 
    # where value should go in sorted array
    frequency = [0] + frequency
    # Get a temporary list to hold result since we can't modify 
    # source while iterating over it
    sorted_data = [ data for data in to_sort ]
    for data in to_sort:
        try:
            freq_index = data[index] + offset
        except IndexError:
            freq_index = 0
        dest = frequency[freq_index]
        frequency[freq_index] += 1
        sorted_data[dest] = data
    # Copy result back into source
    for i in range(len(to_sort)):
        to_sort[i] = sorted_data[i]

def is_sum_of_two_from(n: int, numbers: List[int]) -> bool:
    """Can n be expressed as a sum of two numbers from numbers?
    Note allows one number to be used twice
    """
    # find number closest to n / 2 by binary search, then scan outward
    high = binary_search_fuzzy(n / 2, numbers)
    low = high
    limit = len(numbers)
    while low > -1 and high < limit:
        guess = numbers[low] + numbers[high]
        if guess > n:
            low -= 1
        elif guess < n:
            high += 1
        else:
            return True
    return False

def binary_search(target, search_in: List) -> int:
    """If target is in search_in, return its index
    if target is not in search_in, say the index where it would be is i, 
    we return -(i + 1)
    """
    low = 0
    high = len(search_in)
    while low < high:
        mid = (low + high) // 2
        value = search_in[mid]
        if value > target:
            high = mid
        elif value < target:
            low = mid + 1
        else:
            return mid
    return -1 * (low + 1)

def binary_search_fuzzy(target, search_in) -> int:
    """Find index of target in search_in, or index where it would be."""
    i = binary_search(target, search_in)
    return -(i + 1) if i < 0 else i

def binary_search_less_close(
    target, min: int, max: int, func: Callable[[int], float]
    ) -> int:
    """Find the int in the specified range which, when passed 
    through the provided function, gives a result closest to 
    but less than target
    """
    low = min
    high = max + 1
    while low < high:
        mid = (low + high) // 2
        value = func(mid)
        if value > target:
            high = mid
        elif value < target:
            low = mid + 1
        else:
            return mid - 1
    return low if value < target else low - 1

def lexilogical_permutation_generator(characters: str) -> Generator:
    """Given a string of unique characters, returns a generator which will yield
    each permutation of the characters in lexilogical order.
    """
    as_list = [c for c in characters]
    as_list.sort()
    yield "".join(as_list)
    length = len(as_list)
    while True:
        # scan to find first where left is smaller than right
        i = length - 2
        while i > -1 and as_list[i] > as_list[i + 1]:
            i -= 1
        if i == -1:
            return
        # swap it with the next largest from the right
        swap_with = i + 1
        for j in range(i + 2, length):
            if as_list[swap_with] > as_list[j] > as_list[i]:
                swap_with = j
        as_list[i], as_list[swap_with] = as_list[swap_with], as_list[i]
        # reverse the part to the right
        as_list[i + 1:] = reversed(as_list[i + 1:])
        yield "".join(as_list)

def lexographic_permutation(characters: str, n: int) -> str:
    """ Get the nth lexographic permutation of characters"""
    chars = [ c for c in characters ]
    chars.sort()
    fact = to_factoradic_array(n)
    indices = [0] * (len(characters) - len(fact))
    indices.extend(fact)
    res = ""
    for i in range(len(indices)):
        res += chars[indices[i]]
        del chars[indices[i]]
    return res

def to_factoradic_array(n: int) -> List[int]:
    """ Convert number to factoradic base. 
    Returns as array of ints where the place value of each 
    int in the array is (length - i - 1)!
    """
    res = [ 0 ]
    f = 2
    while n > 0:
        res.append(n % f)
        n //= f
        f += 1
    res.reverse()
    return res

def fibonacci_generator() -> Generator:
    """ Generator yielding elements of the Fibonacci sequence
    starting with 0
    """
    a = 0
    b = 1
    yield a
    yield b
    while True:
        a += b
        yield a
        b += a
        yield b

def combination_count(n: int, r: int, fact_gen: Factorial = None) -> int:
    """ How many ways are there to pick r elements 
    from n elements with no repeats 
    """
    if fact_gen:
        n_fact = fact_gen.get(n)
        r_fact = fact_gen.get(r)
        n_r_fact = fact_gen.get(n - r)
        return n_fact // (r_fact * n_r_fact)
    return math.factorial(n) // (math.factorial(r) * math.factorial(n - r))

def combinations_in_order(elements: List, n: int) -> Generator:
    """ Return every combination of n elements from elements
    including repeat elements and return in sorted order.
    """
    n_elements = len(elements)
    # Keeps track of which element from elements is in which 
    # position via its index in elements
    current_i = [ 0 ] * n
    # Helper to convert back into given elements
    def to_values():
        return [ elements[i] for i in current_i ]
    yield to_values()
    while True:
        # Increment first digit
        i = 0
        current_i[i] += 1
        # Do carries as necessary
        while current_i[i] == n_elements:
            i += 1
            try:
                current_i[i] += 1
            except IndexError:
                # Means we've reached the end
                return
        # [0, 1] == [1, 0] for combinations, 
        # so next after [1, 0] is [1, 1]
        v = current_i[i]
        for j in range(i):
            current_i[j] = v
        yield to_values()

def binary_array_count(size: int) -> Generator[List[int], None, None]:
    """ Yield a series of arrays of given size representing
    successive binary numbers
    """
    current = [0] * size
    yield current
    while True:
        # increment last digit
        i = -1
        current[i] += 1
        # do carries as necessary
        while current[i] > 1:
            current[i] = 0
            i -= 1
            if (size + i) < 0:
                return
            current[i] += 1
        yield current

def combinations_no_repeats(elements: List, n: int) -> Generator[List, None, None]:
    """ Yield every subset of elements of size n as a list """
    length = len(elements)
    indices = [ i for i in range(n) ]
    def i_to_elem():
        return [ elements[i] for i in indices ]
    def reset(to: int):
        for i in range(to):
            indices[i] = i
    yield i_to_elem()
    while True:
        c = 0
        while c < n - 1 and indices[c] == (indices[c + 1] - 1):
            c += 1
        indices[c] += 1
        if indices[c] == length:
            return
        reset(c)
        yield i_to_elem()

def permute_pick_n(elements: List, n) -> Generator[List, None, None]:
    """ for each subset of elements of size n
    yield each permutation of that subset
    """
    for combo in combinations_no_repeats(elements, n):
        for perm in permute(combo):
            yield perm

def permute(input: List) -> Generator:
    """ Gererate all permutations of the elements in input
    using Heap's Algorithm
    Note these will not be in lexiographic order
    Note this permutes the input in-place
    """
    return heap_help(len(input), input)

def heap_help(k: int, input: List) -> Generator:
    if k == 1:
        yield input
    else:
        yield from heap_help(k - 1, input)
        for i in range(k - 1):
            swap = 0 if k % 2 else i
            input[swap], input[k - 1] = input[k - 1], input[swap]
            yield from heap_help(k - 1, input)

def is_permutation(a: List, b: List) -> bool:
    if len(a) != len(b):
        return False
    a_freq: Dict = {}
    for elem in a:
        if elem in a_freq:
            a_freq[elem] += 1
        else:
            a_freq[elem] = 1
    for elem in b:
        if elem not in a_freq:
            return False
        else:
            a_freq[elem] -= 1
    for elem in a_freq:
        if a_freq[elem]:
            return False
    return True

def int_array_to_int(ints: List[int]) -> int:
    """ Convert an array of ints represening digits of 
    a number(should be single-digit)
    to that number by concatinating.
    """
    return int("".join([str(d) for d in ints]))

def int_array_to_int2(ints: List[int]) -> int:
    """ Convert an array of ints represening digits of 
    a number(should be single-digit)
    to that number by summing values.
    """
    result = 0
    radix = 1
    for i in range(-1, -1 * len(ints) - 1, -1):
        result += ints[i] * radix
        radix *= 10
    return result

def int_to_int_array(n: int) -> List[int]:
    """ Convert an int into an array of the ints at each digit """
    return to_array_base(n, 10)

def to_array_base(n: int, r: int) -> List[int]:
    """ Convert an int into an array of the ints at each digit
    where the radix for the output is given by r.
    e.g. to_array_base(6, 2) converts 6 to it's binary array 
    representation: [1, 1, 0]
    """
    result = [ n % r ]
    n //= r
    while n > 0:
        result.append(n % r)
        n //= r
    result.reverse()
    return result

def digital_sum(n: int) -> int:
    result = n % 10
    n //= 10
    while n > 0:
        result += n % 10
        n //= 10
    return result

def count_digits(n: int) -> int:
    n = abs(n)
    result = 1
    n //= 10
    while n != 0:
        result += 1
        n //= 10
    return result

def factorials(n: int) -> List[int]:
    """ Return an array where the ith element is i! """
    facts = [0] * (n + 1)
    facts[0] = 1
    for i in range(1, len(facts)):
        facts[i] = facts[i - 1] * i
    return facts

def rotate(a: List) -> List:
    """ Rotate all elements one to the right in place """
    temp = a[-1]
    for i in range(len(a) - 1, -1, -1):
        a[i] = a[i - 1]
    a[0] = temp
    return a

def rotations(a: List) -> Generator:
    """ Yield all rotations of the givin array where each is 
    rotated once more to the right 
    """
    yield a
    for i in range(len(a) - 1):
        yield rotate(a)

def is_palindrome(a: List) -> bool:
    """ Check if the elements in a list are palindromic """
    size = len(a)
    if size == 1:
        return True
    is_pal = True
    for i in range(size // 2):
        if not a[i] == a[size - 1 - i]:
            is_pal = False
            break
    return is_pal

def get_palindromes(max_digits: int) -> Generator:
    """ Yield all base 10 numbers which are palindromes in order """
    if max_digits < 1:
        return
    # first the trivial single-digits
    for n in range(10):
        yield n
    # We'll effectively be incrementing the first half of the 
    # palindrome and just reversig it for the second half
    # We do this one digit size at a time to return them in order
    half_size = 1 # how many digits in half the palindrome
    s = 1 # which means a range from s to e exclusive
    e = 10
    # the odd number digit palindromes are more efficient
    # to calculate along with the even, but save them in a fifo 
    # queue for later so we return in order
    q = [] 
    while True:
        if (2 * half_size) > max_digits:
            return
        for n in range(s, e):
            first_part = int_to_int_array(n)
            last_part = [ r for r in reversed(first_part) ]
            yield int_array_to_int(first_part + last_part)
            if (2 * half_size + 1) <= max_digits:
                for m in range(10):
                    q.append(int_array_to_int(first_part + [m] + last_part))
        for n in q:
            yield n
        # initilize for next loop
        half_size += 1
        s *= 10
        e *= 10
        q = []

def is_pandigital(n: int) -> bool:
    has_digits = [False] * 10
    has_digits[0] = True
    count = 1
    while n:
        count += 1
        has_digits[n % 10] = True
        n //= 10
    for i in range(count):
        if not has_digits[i]:
            return False
    return True

def sum_character_numbers(input: str) -> int:
    result = 0
    for c in input:
        result += character_number(c)
    return result

def character_number(c: str) -> int:
    if len(c) != 1:
        raise ValueError
    return ord(c.capitalize()) - 64

def square_root_continued_fraction_notation(n: int) -> List[int]:
    """ Return the continued fraction representation 
    of the square root of n.
    Note the second through last elements of the returned list 
    should be considered to repeat infinitely.
    """
    # set up
    a0 = math.floor(math.sqrt(n))
    m = a0
    d = 1
    result: List[int] = [ a0 ]

    # first
    d = n - (m * m) // d
    if not d:
        # n is perfect square, skip
        return result

    a = (a0 + m) // d
    result.append(a)
    m = a * d - m
    cycle_start = (d, a, m)

    while True:
        d = (n - (m * m)) // d
        a = (a0 + m) // d
        m = a * d - m
        if (d, a, m) == cycle_start:
            break
        result.append(a)
    return result

def continued_fraction_notation_to_generator(notation: List[int]) \
    -> Generator[int, None, None]:
    """ For a continued fraction representation the second through last
    terms should be considered to repeat infinitely.
    This returns an infinite generator given that finite representation.
    """
    yield notation[0]
    if len(notation) == 1:
        return
    while True:
        for i in range(1, len(notation)):
            yield notation[i]

def square_root_continued_fraction_generator(n: int) \
    -> Generator[int, None, None]:
    return continued_fraction_notation_to_generator(
        square_root_continued_fraction_notation(n))

def convergent_generator(notation: Generator[int, None, None]) \
    -> Generator[Frac, None, None]:
    """ Yield successive convergents given the continued 
    fraction representation
    See the below link for the recursive relation used here
    https://en.wikipedia.org/wiki/Continued_fraction#Infinite_continued_fractions_and_convergents
    """
    try:
        f_2 = Frac(1, 0)
        f_1 = Frac(next(notation), 1)
        yield f_1
        while True:
            a = next(notation)
            f = Frac(a * f_1.n + f_2.n, a * f_1.d + f_2.d)
            yield f.simplify()
            f_2 = f_1
            f_1 = f
    except StopIteration:
        return

def square_root_convergent_generator(n: int) -> Generator[Frac, None, None]:
    return convergent_generator(square_root_continued_fraction_generator(n))

def babyl_sqrt(n: int) -> int:
    """ Return the integer approximation of the square root of n
    If the result is exact, result is positive, else negative
    """
    if n == 0 or n == 1:
        return True
    guess = n >> 1
    seen: Set[int] = set([guess])
    while guess * guess != n:
        guess = (guess + n // guess) >> 1
        if guess in seen:
            return -1 * guess
        seen.add(guess)
    return guess

def primitive_pythagorean_triplets(m_limit: int = 0) \
    -> Generator[Tuple[int, int, int], None, None]:
    """ Generates primitive pythagorean triplets
    These are tuples of integers a, b, c such that a^2 + b^2 = c^2
    and a, b, and c have no common factor.
    Optionally, provide a value of m which generating values should 
    remain below.
    https://en.wikipedia.org/wiki/Pythagorean_triple#Generating_a_triple
    """
    m = 2
    m_sq = m * m
    while True:
        for n in range(1, m):
            if (m + n) & 1 and gcd(m, n) == 1:
                n_sq = n * n
                a = m_sq - n_sq
                b = 2 * m * n
                yield (min(a, b), max(a, b), m_sq + n_sq)
        m += 1
        if m_limit and m == m_limit:
            return
        m_sq = m * m

def dijkstra_min_path_length(nodes: Set[Node], start: Node, end: Node):
    ''' Use Dijkstra's algorithm to find the lowest cost for traversing the
    graph of nodes from start to end, where the cost for passing though
    each node is its value. (Note one often assigns cost to graph edges, 
    that is not the case, here)
    '''
    # Store shortest path from start to each node, so far
    shortest_path_to = dict()
    max_val = sys.maxsize
    for node in nodes:
        # Set all to practical infinity, so first check will store a value
        shortest_path_to[node] = max_val
    # Length from start to start is its value
    shortest_path_to[start] = start.value
    # set unvisited_nodes as a min-heap by shortest path
    unvisited = Heap(lambda a, b: shortest_path_to[a] - shortest_path_to[b], nodes)
    while unvisited.get_root():
        # Get the node closest to start
        cur_node = unvisited.pop_root()
        path_val = shortest_path_to[cur_node]
        # See if we can update distance to each of it's children
        for child in cur_node.children:
            new_value = path_val + child.value
            if new_value < shortest_path_to[child]:
                shortest_path_to[child] = new_value
                unvisited.update(child)
    # Once we've visited all nodes, the value at end should be correct
    return shortest_path_to[end]

def quadratic_formula(a: float, b: float, c: float) -> Tuple[float, float]:
    disc = b * b - (4 * a * c)
    if disc < 0:
        raise ValueError
    sqrt_disc = math.sqrt(disc)
    return (
        (-1 * b + sqrt_disc) / (2 * a),
        (-1 * b - sqrt_disc) / (2 * a),
            )

if __name__ == '__main__':
    """starts here"""
    start = time.time()

    # for c in permute_pick_n([0, 1, 2, 3], 3):
    #     print(c)
    print(len(list(permute_pick_n([0, 1, 2, 3], 3))))
    print(time.time() - start)
