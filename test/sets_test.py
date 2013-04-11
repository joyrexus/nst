from ..sets import *
from nose.tools import with_setup

A, B, C, U = None, None, None, None

def base_sets():
    global A, B, C, U
    A = Set(['a', 'b', 'c'])
    B = Set(['c', 'd', 'e'])
    C = Set(['a', 'd', 'e'])
    U = Universe()

@with_setup(base_sets)
def test_set():
    '''Testing basic Set object properties'''
    assert A == ['a', 'b', 'c']
    assert A != ['a', 'b']
    assert A != ['a', 'b', 'c', 'd']
    assert A == Set(['a', 'a', 'b', 'b', 'c', 'c'])
    assert A == Set(['c', 'b', 'a'])
    assert len(A) == 3
    assert B == ['c', 'd', 'e']
    assert B == Set(['c', 'c', 'd', 'd', 'e', 'e'])
    assert B == Set(['e', 'd', 'c'])
    assert len(B) == 3
    assert len(A) == len(B)
    assert all(x in A for x in 'a b c'.split())

    X = Set([A, B])
    assert A in X
    assert B in X
    assert X == Set([['a', 'b', 'c'], ['c', 'd', 'e']])
    assert X == Set([Set(['a', 'b', 'c']), Set(['c', 'd', 'e'])])

def test_nested():
    '''Testing nested Sets'''
    X = Set([['a']])
    Y = Set([['a', 'b']])
    assert ['a'] in X
    assert ['a', 'b'] in Y
    assert not ['a', 'b'] in X
    assert not Y in X
    assert not X in Y
    Z = Set([X, Y])
    assert X in Z
    assert Y in Z
    assert not Z in Z

@with_setup(base_sets)
def test_union():
    '''Testing union method'''
    assert A.union(B) == ['a', 'b', 'c', 'd', 'e']
    assert A | B == ['a', 'b', 'c', 'd', 'e']

    assert B.union(A) == ['a', 'b', 'c', 'd', 'e']
    assert B | A == ['a', 'b', 'c', 'd', 'e']

    assert A.union(B, C) == ['a', 'b', 'c', 'd', 'e']
    assert A | B | C == ['a', 'b', 'c', 'd', 'e']

    X = Set(['x'])
    assert A.union(B, X) == ['a', 'b', 'c', 'd', 'e', 'x']
    assert A | B | X == ['a', 'b', 'c', 'd', 'e', 'x']

@with_setup(base_sets)
def test_intersect():
    '''Testing intersect method'''
    assert A.intersect(B) == ['c']
    assert A & B == ['c']
    assert B.intersect(A) == ['c']
    assert B & A == ['c']
    assert C.intersect(B) == ['d', 'e']
    assert C & B == ['d', 'e']
    assert B.intersect(C) == ['d', 'e']
    assert B & C == ['d', 'e']
    assert A.intersect(B, C) == []
    assert A & B & C == []

@with_setup(base_sets)
def test_powerset():
    '''Testing powerset method'''
    P = A.powerset()
    assert len(A) == 3
    assert len(P) == 2**len(A)
    assert len(P) == 8
    assert all(Set(x) in P for x in ([], ['a'], ['a', 'b']))
    assert P == Set([[], 
                     ['a'], ['b'], ['c'], 
                     ['a', 'b'], ['a', 'c'], ['b', 'c'],
                     ['a', 'b', 'c']])
    assert P == [Set([]), 
                 Set(['a']), 
                 Set(['a', 'b']), 
                 Set(['a', 'b', 'c']), 
                 Set(['a', 'c']), 
                 Set(['b']), 
                 Set(['b', 'c']), 
                 Set(['c'])]
    for a, b in zip(A.powergen(), A.powerset()): assert a == b

@with_setup(base_sets)
def test_product():
    '''Testing product method'''
    X = A.product(B)
    print X
    assert X == A * B
    assert len(X) == len(A) * len(B)
    assert ('a', 'e') in X
    assert ('b', 'e') in X
    assert ('c', 'e') in X
    assert ('a', 'a') not in X

@with_setup(base_sets)
def test_containment():
    '''Testing issubset and issuperset methods'''
    assert A.equals(A)
    assert A == A
    assert A.issubset(A)
    assert A <= A
    assert not A.issubset(A, proper=True)
    assert not A < A
    assert A.issuperset(A)
    assert A >= A
    assert not A.issuperset(A, proper=True)
    assert not A > A

    S = Set(['a', 'b', 'c', 'd'])
    assert not A.equals(S)
    assert A != S
    assert A.issubset(S)
    assert A <= S
    assert A.issubset(S, proper=True)
    assert A < S
    assert not A.issuperset(S)
    assert not A > S

    assert not S.issubset(A)
    assert not S < A
    assert S.issuperset(A)
    assert S >= A
    assert S.issuperset(A, proper=True)
    assert S > A

@with_setup(base_sets)
def test_difference():
    '''Testing difference method'''
    assert A == ['a', 'b', 'c']
    assert B == ['c', 'd', 'e']
    assert C == ['a', 'd', 'e']

    assert A.difference(B) == ['a', 'b']
    assert A - B == ['a', 'b']
    assert B.difference(A) == ['d', 'e']
    assert B - A == ['d', 'e']

    assert A - C == ['b', 'c']
    assert C - A == ['d', 'e']

@with_setup(base_sets)
def test_sym_diff():
    '''Testing symmetric difference method'''
    assert B - C == ['c']
    assert C - B == ['a']
    assert B ^ C == ['a', 'c']
    assert B ^ C == (B | C) - (C & B)
    assert B ^ C == (B - C) | (C - B)

@with_setup(base_sets)
def test_disjoint():
    '''Testing isdisjoint method'''
    assert A & B == ['c']
    assert not A.isdisjoint(B)
    X = Set(['x1', 'x2'])
    Y = Set(['y1', 'y1'])
    assert A.isdisjoint(X)
    assert A.isdisjoint(X, Y)
    assert X.isdisjoint(Y)
    assert not X.isdisjoint(X)

@with_setup(base_sets)
def test_universe():
    '''Testing complementation with Universe'''
    assert 'a' not in U - A
    assert 'a' not in U - A | B
    assert 'a' in U - A | A
    assert 'x' in U - A
    assert (U - A) & (U - B) == U - (A | B)
    assert (U - A) | B == U - (A - B)
    NOT = Universe()
    assert NOT-A & NOT-B == NOT-(A | B)
    assert NOT-A | B == NOT-(A - B)
    assert NOT - (NOT-A) == A
    assert NOT - (NOT - (NOT-A)) == NOT-A

@with_setup(base_sets)
def test_complements():
    '''Testing complementation with __invert__ method'''
    assert 'a' in A
    assert 'a' not in ~A
    assert 'a' not in ~A | B
    assert 'x' in ~A
    assert ~A == U - A
    assert ~A & ~B == ~(A | B)
    assert ~A | B == ~(A - B)
    assert ~~A == A
    assert ~~~A == ~A

def test_relation():
    '''Testing relation constructor method.'''
    X = Set([1, 2, 3])
    cond = lambda a, b: a < b
    R = X.relation(cond)
    assert R == Set([(1, 2), (1, 3), (2, 3)])

    A = Set(['a', 'b', 'c'])
    R = A.relation(cond)
    assert R == [('a', 'b'), ('a', 'c'), ('b', 'c')]

    A = Set(['a', 'b'])
    P = A.powerset()
    R = P.relation(cond)
    assert len(P) == 2 ** len(A)
    assert R == [([], ['a']), 
                 ([], ['b']), 
                 ([], ['a', 'b']), 
                 (['a'], ['a', 'b']), 
                 (['b'], ['a', 'b'])]

    order_by_inclusion = lambda x, y: x <= y
    R = P.relation(order_by_inclusion)
    assert R.reflexive
    assert R.antisymmetric
    assert R.transitive
    assert R.partial_order

    Z = Set([(x, y) for x in range(-2, 2) for y in range(-2, 2)])
    def z(x, y): return float(2*x + 1) / 2**y
    cond = lambda a, b: z(*a) <= z(*b)
    R = Z.relation(cond)
    assert R.reflexive
    assert not R.symmetric
    assert R.transitive
    assert R.antisymmetric
    assert R.partial_order
    assert not R.total_order

def test_relations():
    '''Testing Relations'''
    X = Set(['a', 'b', 'c', 'd', 'e'])
    R = Relation([('a', 'a'), ('b', 'b'), ('c', 'c'), 
                  ('a', 'b'), ('b', 'c'), ('a', 'c'), 
                  ('b', 'a'), ('c', 'b'), ('c', 'a'),
                  ('d', 'd'), ('e', 'e'),
                  ('d', 'e'), ('e', 'd')])

    assert R.domain == X
    assert R.range == X
    assert R.reflexive
    assert R.symmetric
    assert R.transitive
    assert not R.antisymmetric
    assert not R.partial_order

    A  = Relation([('a', 'a'), ('b', 'b'), ('c', 'c'),
                   ('b', 'c'), ('a', 'c')])
    A_ = Relation([('a', 'a'), ('b', 'b'), ('c', 'c'),
                   ('c', 'b'), ('c', 'a')])
    assert A.inverse == A_
    a = A.element('a')
    b = A.element('b')
    c = A.element('c')
    assert c.immediate_predecessors() == Set([a, b])
    assert A.first == None
    assert A.last == A.element('c')
    assert A_.first == A.element('c')
    assert A_.last == None

    B = Relation([('a', 'a'), ('b', 'b'), ('c', 'c'),
                  ('a', 'b'), ('b', 'c'), ('a', 'c')])
    assert B.comparable
    assert B.reflexive
    assert not B.symmetric
    assert B.antisymmetric
    assert B.transitive
    assert B.partial_order
    assert B.total_order
    assert B.first == B.element('a')
    assert B.last == B.element('c')

    assert B.maximals == Set(['c'])
    assert B.minimals == Set(['a'])

    C = Relation([('a', 'a'), ('b', 'b'), 
                  ('a', 'b'), ('b', 'c'), ('a', 'c')])
    assert not C.comparable
    assert not C.reflexive
    assert not C.symmetric
    assert C.antisymmetric
    assert C.transitive
    assert not C.partial_order
    assert not C.total_order

    D = Relation([('a', 'a'), ('b', 'b'), ('c', 'c'), ('d', 'd'),
                  ('a', 'b'), ('b', 'c'), ('a', 'c')])
    assert D.reflexive
    assert not D.symmetric
    assert D.antisymmetric
    assert D.transitive
    assert D.partial_order
    assert not D.total_order

    assert D.maximals == Set(['c', 'd'])
    assert D.minimals == Set(['a', 'd'])

    assert D.predecessors('a') == Set(['a'])
    assert D.predecessors('b') == Set(['a', 'b'])
    assert D.predecessors('c') == Set(['a', 'b', 'c'])

    assert D.predecessors('a', strict=True) == Set()
    assert D.predecessors('b', strict=True) == Set(['a'])
    assert D.predecessors('c', strict=True) == Set(['a', 'b'])

    assert D.predecessors('a') < D.predecessors('b')
    assert not D.predecessors('b') < D.predecessors('a')

    a = D.element('a')
    b = D.element('b')
    c = D.element('c')
    assert 'a' == OrderedElement('a', D)
    assert 'b' == OrderedElement('b', D)
    assert 'c' == OrderedElement('c', D)
    assert a < b
    assert a < c
    assert a < b < c
    assert not a > b
    assert not b > c
    assert not a > b > c
    assert a <= b
    assert not a >= b
    assert not a == b
    assert a == a
    assert b == b
    assert b.between(a, c)
    assert b.between(a, b)
    assert not b.between(a, b, strict=True)

    assert a.predecessors() == Set()
    assert b.predecessors() == Set([a])
    assert c.predecessors() == Set([a, b])
    assert c.prev() == b
    assert b.prev() == a
    assert a.prev() == None

    assert a.successors() == Set([b, c])
    assert b.successors() == Set([c])
    assert c.successors() == Set()
    assert a.next() == b
    assert b.next() == c
    assert c.next() == None

def test_equivalence_rels():
    '''Testing equivalence relations'''
    R = Relation([('a', 'a'), ('b', 'b'), ('c', 'c'), 
                  ('a', 'b'), ('b', 'c'), ('a', 'c'), 
                  ('b', 'a'), ('c', 'b'), ('c', 'a'),
                  ('d', 'd'), ('e', 'e'),
                  ('d', 'e'), ('e', 'd')])

    assert R.equivalence_classes == [['a', 'b', 'c'], ['d', 'e']]

def test_partitions():
    '''Testing Partitions'''
    C = Partition([Set(['a', 'b', 'c']), Set(['d', 'e'])])
    R = Relation([('a', 'a'), ('b', 'b'), ('c', 'c'), 
                  ('a', 'b'), ('b', 'c'), ('a', 'c'), 
                  ('b', 'a'), ('c', 'b'), ('c', 'a'),
                  ('d', 'd'), ('e', 'e'),
                  ('d', 'e'), ('e', 'd')])

    assert R == C.equivalence_relation
    assert R.equivalence_classes == [['a', 'b', 'c'], ['d', 'e']]

    X = Set(['a', 'b', 'c', 'd', 'e'])
    assert R == X/C

    assert R == X / Partition(X/R)
    assert C == R.equivalence_classes
    assert C == X/R
    assert C == X / Relation(X/C)

    assert 'a'/R == ['a', 'b', 'c']
    assert 'd'/R == ['d', 'e']
    assert X/R == [['a', 'b', 'c'], ['d', 'e']]
    assert R.equivalence_classes == [['a', 'b', 'c'], ['d', 'e']]
    assert 'a'/(X * X) == X, 'X is only equiv class'

def test_sample_space():
    '''Testing SampleSpace probability'''
    A = Set(['a', 'b', 'c'])
    B = Set(['c', 'd'])
    C = Set(['d', 'e', 'f'])
    P = SampleSpace(A, B, C)
    assert P(A) == 0.5
    assert "{:.3}".format(P(B)) == '0.333'
    assert P(C) == 0.5
    assert "{:.3}".format(P(A & B)) == '0.167'
    assert P(A & C) == 0.0
    assert "{:.3}".format(P(A | B)) == '0.667'
    assert P(A | C) == 1.0
    assert P(A, given=B) == 0.5
    assert P(A, given=C) == 0.0
    assert P(A & B) == P(A, given=B) * P(B)
