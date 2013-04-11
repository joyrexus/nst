class Set(list):
    '''
    Representation of a set.
    
    '''
    def __init__(self, seq=[], reduce=True):
        members = []
        if reduce:
            for i in seq: 
                if i not in members: members.append(i) 
        else:
            members = list(seq)
        super(Set, self).__init__(sorted(members))

    def __and__(self, X):
        return self.intersect(X)

    def __or__(self, X):
        return self.union(X)

    def __sub__(self, X):
        return self.difference(X)

    def __mul__(self, X):
        return self.product(X)

    def __xor__(self, X):
        return self.union(X) - self.intersect(X)

    def __lt__(self, X):
        return self.issubset(X, proper=True)

    def __le__(self, X):
        return self.issubset(X)

    def __gt__(self, X):
        return self.issuperset(X, proper=True)

    def __ge__(self, X):
        return self.issuperset(X)

    def __eq__(self, X):
        return all(x in self for x in X) and all(x in X for x in self)

    def __invert__(self):
        U = Universe()
        return U - self

    def add(self, x):
        if x not in self:
            self.append(x)

    def equals(self, X): 
        if len(self) != len(X):
            return False
        elif self.intersect(X) == self:
            return True 
        else:
            return False

    def issubset(self, X, proper=False):
        return X.issuperset(self, proper)

    def issuperset(self, X, proper=False):
        if proper:
            if not len(self) > len(X):
                return False
        else:
            if not len(self) >= len(X):
                return False
        for i in X:
            if i not in self:
                return False
        return True

    def isdisjoint(self, *sets):
        if self.intersect(*sets):
            return False
        else:
            return True

    def update(self, *sets):
        return self.union(*sets)

    def union(self, *sets):
        sets = self + list(sets)
        return Set(i for S in sets for i in S)

    def intersect(self, *sets):
        if not sets:
            return self
        else:
            first, rest = sets[0], sets[1:]
            I = [i for i in first if i in self.intersect(*rest)]
            return Set(I, reduce=False)

    def difference(self, X): 
        return Set((i for i in self if i not in X), reduce=False)

    def product(self, X):
        return Relation([(i, j) for j in X for i in self], reduce=False)

    def powergen(self, set=None):
        if set is None: set = self
        if set:
            head, rest = set[:1], set[1:]
            for e in self.powergen(rest):
                yield Set(e)
                yield Set(head + e)
        else:
            yield Set()

    def powerset(self, set=None):
        return Set(self.powergen(), reduce=False)

    def relation(self, cond):
        '''
        Return a Relation consisting of a set
        of tuples. Each tuple consists of two
        elements of the set in the specified condition.

        '''
        return Relation([(a, b) for a in self 
                                for b in self if cond(a, b)])


class Universe(object):
    '''
    Universe has a set-like interface and implements set 
    operations consistently on the complements of finite sets.
    
    '''
    def __init__(self):
        self._diff = Set()
 
    def __sub__(self, other):
        S = Universe()
        if type(other) == Set:
            S._diff = self._diff | other
            return S
        if type(other) == Universe:
            return other._diff
        else:
            S._diff = self._diff | other._diff
            return S
 
    def __rsub__(self, other):
        return other & self._diff
 
    def __contains__(self, obj):
        return not obj in self._diff
 
    def __and__(self, other):
        return other - self._diff
 
    def __rand__(self, other):
        return other - self._diff
 
    def __repr__(self):
        if self._diff == Set():
            return "Universe"
        else:
            return "Universe - {0}".format(self._diff)
 
    def __or__(self, other):
        S = Universe()
        S._diff = self._diff - other
        return S
 
    def __xor__(self, other):
        return (self - other) | (other - self)
 
    def add(self, elem):
        if elem in self._diff:
            self._diff.remove(elem)
 
    def update(self, other):
        self._diff = self._diff - other
 
    def __ror__(self, other):
        return self.__or__(other)
 
    def union(self, other):
        return self.__or__(other)
 
    def difference(self, other):
        return self.__sub__(other)
 
    def intersection(self, other):
        return self.__and__(other)
 
    def symmetric_difference(self, other):
        return self.__xor__(other)
 
    def issubset(self, other):
        if type(other) == Set:
            return False
        if issubset(other._diff, self._diff):
            return True
        return False
 
    def issuperset(self, other):
        if self._diff & other:
            return False
        return True
 
    def __lt__(self, other):
        return self.issubset(other)
 
    def __eq__(self, other):
        if type(other) == Set:
            return False
        try:
            return self._diff == other._diff
        except AttributeError:
            return False
 
    def __ne__(self, other):
        return not self.__eq__(other)
 
    def __le__(self, other):
        return self.__lt__(other) or self.__eq__(other)
 
    def __gt__(self, other):
        return self.issuperset(other)
 
    def __gt__(self, other):
        return self.issuperset(other) or self == other

    def __invert__(self):
        return self._diff


class OrderedElement(object):
    '''
    Representation of an element x of some set X based on 
    a partial order R on X.

    '''
    def __init__(self, x, R):
        self.x = x
        self.R = R

    def __eq__(self, y):
        return self.x == y

    def __ne__(self, y):
        return self.x != y

    def __lt__(self, y):
        return self.x != y and (self.x, y) in self.R

    def __le__(self, y):
        return (self.x, y) in self.R

    def __bool__(self):
        return self.x

    def __repr__(self):
        return self.x

    def between(self, m, n, strict=False):
        if strict: 
            return m < self < n
        else:
            return m <= self <= n

    def predecessors(self, strict=True):
        if strict: 
            return Set(e for e in self.R.elements if e < self)
        else:
            return Set(e for e in self.R.elements if e <= self)

    def immediate_predecessors(self):
        '''Return the set of immediate predecessors.'''
        P = self.predecessors(strict=True)
        return Set(p for p in P if not any(p < q < self for q in P))

    def prev(self):
        '''Return an immediate predecessor.'''
        P = self.predecessors(strict=True)
        for p in P:
            if not any(p < q < self for q in P):
                return p

    def successors(self, strict=True):
        return Set(e for e in self.R.elements if e > self)

    def next(self):
        '''Return an immediate successor.'''
        S = self.successors(strict=True)
        for s in S:
            if not any(self > q > s for q in S):
                return s


class Relation(Set):
    '''
    Representation of a binary relation.
    
    '''
    def __init__(self, seq, **kwargs):
        for i in seq: 
            assert type(i) is tuple
            assert len(i) == 2
        super(Relation, self).__init__(seq, **kwargs)

    def element(self, x):
        for e in self.elements:
            if x == e: return e

    @property
    def elements(self):
        if hasattr(self, 'elems'):
            return self.elems
        else:
            self.elems = Set(OrderedElement(x, self) 
                                for x in self.domain | self.range)
            return self.elems

    @property
    def domain(self):
        return Set(x for x, y in self)

    @property
    def range(self):
        return Set(y for x, y in self)

    @property
    def inverse(self):
        return Relation([(y, x) for x, y in self])

    @property
    def first(self): 
        E = self.elements
        for e in E:
            if all(e <= x for x in E):
                return e

    @property
    def last(self): 
        E = self.elements
        for e in E:
            if all(x <= e for x in E):
                return e

    @property
    def maximals(self): 
        return Set([x for x in self.range if not self.successors(x, strict=True)])

    @property
    def minimals(self): 
        return Set([x for x in self.domain if not self.predecessors(x, strict=True)])

    def predecessors(self, c, strict=False):
        '''Return {x: x R c}.'''
        return Set(m for m, n in self if n == c 
                                      and (True if not strict else m != n))

    def successors(self, c, strict=False):
        '''Return {x: c R x}.'''
        return Set(n for m, n in self if m == c 
                                      and (True if not strict else m != n))

    def __rdiv__(self, i):
        return self.equivalence_class(i)

    def equivalence_class(self, i):
        # return self.domain
        # return i, self.domain, i == self.domain
        if i == self.domain:
            return self.equivalence_classes
        else:
            return Set(y for x, y in self if x == i)

    @property
    def equivalence_classes(self):
        return Set(x/self for x in self.domain)

    @property
    def comparable(self):
        X = [x for x in self.domain | self.range]
        return all((a, b) in self or (b, a) in self for a in X for b in X)

    @property
    def reflexive(self):
        return all((m, m) in self and (n, n) in self for (m, n) in self)

    @property
    def symmetric(self):
        return all((n, m) in self for (m, n) in self)

    @property
    def antisymmetric(self):
        return all((n, m) not in self for (m, n) in self if n != m)

    @property
    def transitive(self):
        for (x, y) in self:
            for (y_, z) in self:
                if y == y_ and not (x, z) in self: 
                    return False
        return True

    @property
    def partial_order(self):
        return self.reflexive and self.transitive and self.antisymmetric

    @property
    def total_order(self):
        return self.partial_order and self.comparable


class Partition(Set):
    '''
    Representation of a partition on a set.
    
    '''
    def __init__(self, seq, **kwargs):
        for S in seq:
            assert type(S) is Set
        super(Partition, self).__init__(seq, **kwargs)

    @property
    def equivalence_relation(self):
        R = Relation([])
        for S in self:
            R.extend(S * S)
        return R

    def __rdiv__(self, S):
        if self.union(*self) == S:
            return self.equivalence_relation


class SampleSpace(object):
    '''
    Representation of a sample space.

    '''
    def __init__(self, *sets):
        U = Set()
        self.space = U.union(*sets)
        self.size = float(len(self.space))

    def __call__(self, set, given=[]):
        if given:
            return len(set & given) / float(len(given))
        else:
            return len(set) / self.size


if __name__ == '__main__':

    A = Set(['a', 'b', 'c'])
    B = Set(['c', 'd'])
    C = Set(['d', 'e', 'f'])

    P = SampleSpace(A, B, C)

    print "Probability of A is", P(A)
    print "Probability of B is", P(B)
    print "Probability of C is", P(C)
    print "Probability of A and B is", P(A & B)
    print "Probability of A and C is", P(A & C)
    print "Probability of A or B is", P(A | B)
    print "Probability of A or C is", P(A | C)
    print "Probability of A given B is", P(A, given=B)
    print "Probability of A given C is", P(A, given=C)
    assert P(A & B) == P(A, given=B) * P(B)
