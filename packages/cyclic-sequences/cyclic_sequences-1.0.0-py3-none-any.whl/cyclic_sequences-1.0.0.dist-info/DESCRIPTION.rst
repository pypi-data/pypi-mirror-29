Cyclic-Sequences
################


Description
===========

Sequence type objects with cyclic indexing::

      ┌───────────────────────────┐
      │                           ▼
    ┏━│━┳━━━┳━━━┳━╍┅   ┅╍━┳━━━━━┳━━━┳━━━┓
    ┃ ● ┃ 0 ┃ 1 ┃   ⋅⋅⋅   ┃ N-1 ┃ N ┃ ● ┃
    ┗━━━┻━━━┻━━━┻━╍┅   ┅╍━┻━━━━━┻━━━┻━│━┛
          ▲                           │
          └───────────────────────────┘


Content
=======

* class ``CyclicTuple``
    An immutable cyclic sequence based on built-in class *tuple*.

* class ``CyclicList``
    A mutable cyclic sequence based on built-in class *list*.
    Gets two additional methods:

    * ``set_first(elt)``
        Put given element at first position.
    * ``turn(step)``
        Change all elements index of given step (default is 1 unit onward).


Examples
========

The following examples are using CyclicList class for demonstration. CyclicTuple class gets same behaviours.

- Construction from any iterable::

    >>> foo = CyclicList(['a', 'b', 'c', 'd', 'e'])
    >>> foo
    CyclicList(['a', 'b', 'c', 'd', 'e'])

- Gets its specific string representation with chevrons figuring cycling::

    >>> print(foo)
    <['a', 'b', 'c', 'd', 'e']>

- Accessing works like a regular list::

    >>> foo[1]
    'b'
    >>> foo[-4]
    'b'

- Except indexes higher than length wraps around::

    >>> foo[6]
    'b'
    >>> foo[11]
    'b'
    >>> foo[-9]
    'b'

- Slices work and return list objects::

    >>> foo[1:4]
    ['b', 'c', 'd']
    >>> foo[3:0:-1]
    ['d', 'c', 'b']

- Slices work also out of range with cyclic output::

    >>> foo[3:7]
    ['d', 'e', 'a', 'b']
    >>> foo[8:12]
    ['d', 'e', 'a', 'b']
    >>> foo[3:12]
    ['d', 'e', 'a', 'b', 'c', 'd', 'e', 'a', 'b']
    >>> foo[-2:2]
    ['d', 'e', 'a', 'b']
    >>> foo[-7:-3]
    ['d', 'e', 'a', 'b']
    >>> foo[-7:2]
    ['d', 'e', 'a', 'b', 'c', 'd', 'e', 'a', 'b']

- Slices with non unitary steps work also::

    >>> foo[:7:2]
    ['a', 'c', 'e', 'b']
    >>> foo[:7:3]
    ['a', 'd', 'b']
    >>> foo[:7:5]
    ['a', 'a']

- As well for reversed steps::

    >>> foo[1:-3:-1]
    ['b', 'a', 'e', 'd']
    >>> foo[-4:-8:-1]
    ['b', 'a', 'e', 'd']
    >>> foo[-4:-9:-2]
    ['b', 'e', 'c']
    >>> foo[-4:-9:-3]
    ['b', 'd']
    >>> foo[-5:-11:-5]
    ['a', 'a']

- Incoherent slices return empty list::

    >>> foo[11:5]
    []

Edge effects:

- Indexing an empty CyclicList returns an IndexError.

- Indexing on a unique element returns always this element.


