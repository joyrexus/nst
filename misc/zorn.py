'''
A constructive approach to Zorn's Lemma.

The idea is to define a few functions to illuminate the implicit machinery used
in Zorn's Lemma.

Keep in mind that Hasse diagrams provide a nice representation of posets.

'''
def domain(R):
    '''Return the elements from the domain of R.'''
    return set(m for (m, n) in R)

def range(R):
    '''Return the elements from the range of R.'''
    return set(n for (m, n) in R)

def segment(R, c):
    '''
    Given a partial order R defined on X, return {x: x R c}.
    
    '''
    return frozenset(m for m, n in R if n == c)

def segments(R):
    return set((x, segment(R, x)) for x in domain(R))

def inclusion(S):
    '''
    Return an inclusion relation I for the sets s in S.

    The tuple (m, n) is an element of T if m is a subset of n.

    '''
    return set((x, y) for x in S for y in S if x < y)

def chain(R, c):
    '''
    Return a set of subsets of  ...
    
    '''
    pass


if __name__ == '__main__':

    R = set([(0, 0), (0, 1), (0, 2), (0, 3), 
             (1, 1), (1, 2), (1, 3), 
             (2, 2), (2, 3),
             (3, 3)])

    assert segment(R, 1) == frozenset([0, 1])
    assert segment(R, 2) == frozenset([0, 1, 2])

    X = domain(R)
    assert X == set([0, 1, 2, 3])

    assert segments(R) == set([ (0, frozenset([0])),
                                (1, frozenset([0, 1])),
                                (2, frozenset([0, 1, 2])), 
                                (3, frozenset([0, 1, 2, 3])) ])


    print inclusion(range(segments(R)))

