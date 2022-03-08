import math
from typing import Dict, Generator, Set, List, Tuple
from functools import reduce
import time

class Node:
    def __init__(self, value) -> None:
        self.value = value
        self.children: List['Node'] = []

    def __str__(self) -> str:
        return str(self.value)
    
    def __repr__(self) -> str:
        return repr(self.value)

    def report(self) -> str:
        return (str(self.value) + "->[" 
            + ", ".join([ str(c.value) for c in self.children ]) 
            + "]")

class PrimeMachine:
    def __init__(self, initial_max=2048) -> None:
        self.up_to = initial_max
        self.prime_list = prime_sieve(initial_max)
        self.prime_set = set(self.prime_list)

    def __iter__(self):
        return PrimeIterator(self)

    def get(self, nth: int) -> int:
        try:
            return self.prime_list[nth]
        except IndexError:
            self._get_more()
            return self.get(nth)
    
    def _get_more(self) -> None:
        i = len(self.prime_list)
        self.up_to <<= 1
        self.prime_list = prime_sieve(self.up_to, self.prime_list)
        self.prime_set.update(self.prime_list[i:])

    def get_next(self) -> None:
        current = self.up_to + 1
        if not current % 2:
            current += 1
        while True:
            is_prime = True
            for p in self.prime_list:
                if not current % p:
                    is_prime = False
                    break
            if is_prime:
                self.prime_list.append(current)
                self.prime_set.add(current)
                self.up_to = current
                return
            else:
                current += 2

    def is_prime(self, n: int) -> bool:
        if n > self.up_to:
            self._get_more()
            return self.is_prime(n)
        return n in self.prime_set


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

def prime_sieve(n: int, primes: List[int]=[]) -> List[int]:
    """Get list of all primes less than or equal to n using Sieve of Eratosthenes
    Can optionally provide already calculated primes. 
    These should not be missing any in their range
    """
    sieve_start = 2
    is_prime = [True for i in range(n + 1)]
    if len(primes):
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

def triangle_number(nth: int) -> int:
    return nth * (nth + 1) // 2

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
        while current_i[i] == n_elements and i < n_elements:
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

def combinations_no_repeats(elements: List, n) -> Generator[List, None, None]:
    """ Yield every subset of elements of size n as a list """
    length = len(elements)
    for to_pick in binary_array_count(length):
        if sum(to_pick) == n:
            yield [ elements[i] for i in range(length) if to_pick[i] ]

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

if __name__ == '__main__':
    """starts here"""
    # permute_pick_n
    for perm in permute_pick_n(["a", "b", "c"], 3):
        print(perm)