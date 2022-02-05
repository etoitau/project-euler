import math
from typing import Dict, Generator, Set, List, Tuple
from functools import reduce

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
    # itterate over all possible cominations of exponents
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
    # source while itterating over it
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
    """Given a string of unique characters, returns a gereator which will yield
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

if __name__ == '__main__':
    """starts here"""
    n = 5
    s = "abcd"
    print(lexographic_permutation(s, n))