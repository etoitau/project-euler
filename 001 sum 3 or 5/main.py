# If we list all the natural numbers below 10 that are multiples of 3 or 5, 
# we get 3, 5, 6 and 9. The sum of these multiples is 23.
# Find the sum of all the multiples of 3 or 5 below 1000.
# Result: 233168

def sum_3_5(below):
    """main"""
    sum = 0
    for n in range(3, below):
        if not n % 3 or not n % 5:
            sum += n
    return sum
         

if __name__ == '__main__':
    """starts here"""
    print(sum_3_5(1000))