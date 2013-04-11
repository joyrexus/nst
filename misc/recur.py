import sys
sys.setrecursionlimit(10000)

def succ(n): 
    n.add(frozenset(n))
    return n

assert succ(set([frozenset()])) == set([frozenset([frozenset([])]), 
                                                   frozenset([])])

def sum(m, n):
    if n == 0: return m
    return sum(m, n-1) + 1

for i in range(10):
    for j in range(10):
        assert i + j == sum(i, j)

def mul(m, n):
    if m == 0 or n == 0: return 0
    if n == 1: return m
    return sum(mul(m, n-1), m)

for i in range(10):
    for j in range(10):
        assert i * j == mul(i, j)

def exp(m, n):
    if n == 0: return 1
    return exp(m, n-1) * m

for i in range(10):
    for j in range(10):
        assert i ** j == exp(i, j)
        assert 2**i * 2**j == 2 ** (i + j)
        assert (2**i) ** j == 2 ** (i * j)
