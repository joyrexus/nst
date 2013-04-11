from __future__ import division
from package import *

X = Set([(x, y) for x in range(-2, 2) for y in range(-2, 2)])

def z(x, y):
    return (2*x + 1) / 2**y

cond = lambda a, b: z(*a) <= z(*b)

R = X.relation(cond)

assert len(R) == 136
assert R.reflexive
assert not R.symmetric
assert R.transitive
assert R.antisymmetric
assert R.partial_order
assert not R.total_order
