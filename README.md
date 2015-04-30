nst
===

A pythonic implementation of the basic notions and constructs of [naive set theory](http://en.wikipedia.org/wiki/Naive_set_theory).  

The primitives and higher-level concepts defined here are simple and ineffecient.  The aim is conceptual clarification via algorithmic elaboration.  Use python's [native set types](http://docs.python.org/3/library/stdtypes.html?highlight=frozenset#set-types-set-frozenset) for your day-to-day set manipulations.

----

The `sets.py` module is the main show.

See `test/sets_test.py` for an overview of available methods and usage.  The
test suite was written in conjuction with the module.  It serves as the module's
documentation.

The `misc` directory contains a few experiments, some of which we'd like to
roll into the main module after further development.


## To Do

Develop the `SampleSpace` class and add tests for conditional probablity.

Develop a `Poset` class, extending `Relation`.
