'''
In NST Sect 14 (p. 57) Halmos gives three examples of partially ordered sets
with amusing properties to illustrate the various possibilities in their
behavior.

Here we aim to define less_than functions for each example.  Each function
should return a negative value if its first argument is "less than" its 
second, 0 if the two arguments are "equal", and a positive value otherwise.

'''
from __future__ import division
from random import shuffle

ii_unordered = set()
iii_unordered = set()

def i_less_than(M, N):
    (a, b) = M
    (x, y) = N
    p = ((2 * a) + 1) * (2 ** y)
    q = ((2 * x) + 1) * (2 ** b)
    if p <= q: 
        print "Defined for {} since {} <= {}".format((M, N), p, q)
        return True
    else:
        print "Undefined for {} since {} > {}".format((M, N), p, q)

# ordering for relation ii:
#   a < x or (a == x and (b < y or b == y)
#  (a < x or a == x) and (a < x and (b < y or b == y))
# 
# ordering for relation iii:
#  (a < x or a == x) and (b < y or b == y)

def ii_less_than(M, N):
    '''
    Compare two 2-tuples based on lexicographic order.
    
    '''
    (a, b) = M
    (x, y) = N
    if a < x: 
        return True
    elif a == x and (b < y or b == y):
        return True

def iii_less_than(M, N):
    '''
    Compare two 2-tuples based on present order.
    
    Note that unlike lexicographic order, if the first 
    element of the first 2-tuple is not less than or equal 
    to the first element of the second 2-tuple, we do not 
    evaluate the order between the tuples at all.

    '''
    (a, b) = M
    (x, y) = N
    if (a < x or a == x) and (b < y or b == y):
          return True


X = [(a, b) for a in range(10) for b in range(10)]
for a, b in X:
    M = (a, b+1)
    N = (a, b)
    i_less_than(M, N)



# create a shuffled list of 2-tuples
X = [(a, b) for a in range(10) for b in range(10)]
shuffle(X)


S = [(M, N) for M in X for N in X if ii_less_than(M, N)]    # the relation S
T = [(M, N) for M in X for N in X if iii_less_than(M, N)]   # the relation T

print "S:", len(S)
print "T:", len(T)
print list(set(S) - set(T))[:10]

'''
print sorted(X, cmp=i_less_than)
print
print sorted(X, cmp=ii_less_than)
print
print sorted(X, cmp=iii_less_than)
'''

print '-' * 30
print ii_unordered ^ iii_unordered

'''
Another poset example.

See p. 57 of NST where Halmos describes three partially-ordered sets "with some
amusing properties."

'''
def z(x, y):
    return (2*x + 1) / 2**y

def z_over(a, b):
    for x in range(a, b):
        print
        print "x ==", x
        for y in range(a, b):
            print "   z({}, {}) == {}".format(x, y, z(x, y))

z_over(-2, 3)
