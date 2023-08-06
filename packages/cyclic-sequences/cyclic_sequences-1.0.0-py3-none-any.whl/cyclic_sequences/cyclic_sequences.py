#!/usr/bin/env python3
# -*- coding: utf8 -*-


from itertools import cycle


cyclic_doc = """
{classname}() -> new empty {classname}.

{classname}(iterable) -> new {classname} initialized from iterable’s items.

Author : BCL Mary, based on a Chris Lawlor forum publication

**Description**

A {classparent} with cyclic indexing::

      ┌───────────────────────────┐
      │                           ▼
    ┏━│━┳━━━┳━━━┳━╍┅   ┅╍━┳━━━━━┳━━━┳━━━┓
    ┃ ● ┃ 0 ┃ 1 ┃   ⋅⋅⋅   ┃ N-1 ┃ N ┃ ● ┃
    ┗━━━┻━━━┻━━━┻━╍┅   ┅╍━┻━━━━━┻━━━┻━│━┛
          ▲                           │
          └───────────────────────────┘

- Construction from any iterable::

    >>> foo = {classname}(['a', 'b', 'c', 'd', 'e'])
    >>> foo
    {classname}({A}'a', 'b', 'c', 'd', 'e'{Z})

- Gets its specific string representation with chevrons figuring cycling::

    >>> print(foo)
    <{A}'a', 'b', 'c', 'd', 'e'{Z}>

- Iterating is bounded by the number of elements::

    >>> for x in foo: print(x)
    ...
    a
    b
    c
    d
    e

- Accessing works like a regular {classparent}::

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

- Slices work and return {classparent} objects::

    >>> foo[1:4]
    {A}'b', 'c', 'd'{Z}
    >>> foo[2:]
    {A}'c', 'd', 'e'{Z}
    >>> foo[3:0:-1]
    {A}'d', 'c', 'b'{Z}

- Slices work also out of range with cyclic output::

    >>> foo[3:7]
    {A}'d', 'e', 'a', 'b'{Z}
    >>> foo[8:12]
    {A}'d', 'e', 'a', 'b'{Z}
    >>> foo[3:12]
    {A}'d', 'e', 'a', 'b', 'c', 'd', 'e', 'a', 'b'{Z}
    >>> foo[-2:2]
    {A}'d', 'e', 'a', 'b'{Z}
    >>> foo[-7:-3]
    {A}'d', 'e', 'a', 'b'{Z}
    >>> foo[-7:2]
    {A}'d', 'e', 'a', 'b', 'c', 'd', 'e', 'a', 'b'{Z}

- Slices with non unitary steps work also::

    >>> foo[:7:2]
    {A}'a', 'c', 'e', 'b'{Z}
    >>> foo[:7:3]
    {A}'a', 'd', 'b'{Z}
    >>> foo[:7:5]
    {A}'a', 'a'{Z}

- As well for reversed steps::

    >>> foo[1:-3:-1]
    {A}'b', 'a', 'e', 'd'{Z}
    >>> foo[-4:-8:-1]
    {A}'b', 'a', 'e', 'd'{Z}
    >>> foo[-4:-9:-2]
    {A}'b', 'e', 'c'{Z}
    >>> foo[-4:-9:-3]
    {A}'b', 'd'{Z}
    >>> foo[-5:-11:-5]
    {A}'a', 'a'{Z}

- Incoherent slices return empty {classparent}::

    >>> foo[11:5]
    {A}{Z}

Edge effects:

- Indexing an empty {classname} returns an IndexError.

- Indexing on a unique element returns always this element.

"""


cyclic_doc_methods = """
**Methods**

First element can be set using specific methods:

- **set_first**: put given element at first position::

    >>> foo.set_first('c')
    >>> foo
    {classname}({A}'c', 'd', 'e', 'a', 'b'{Z})

- **turn**: change all elements index of given step
  (default is 1 unit onward)::

    >>> foo.turn()
    >>> foo
    {classname}({A}'d', 'e', 'a', 'b', 'c'{Z})
    >>> foo.turn(-3)
    >>> foo
    {classname}({A}'a', 'b', 'c', 'd', 'e'{Z})
    >>> foo.turn(11)
    >>> foo
    {classname}({A}'b', 'c', 'd', 'e', 'a'{Z})

"""


class CyclicBase(object):

    def __repr__(self):
        return "%s(%s)" % (
            self.__class__.__name__,
            self._parent.__repr__(self)
            )

    def __str__(self):
        return "<" + self._parent.__repr__(self) + ">"

    def __getitem__(self, key):
        """x.__getitem__(y) <==> x[y]"""
        N = self.__len__()
        if N == 0:
            raise IndexError(
                '{} is empty'.format(self.__class__.__name__)
                )
        if isinstance(key, int):
            return self._parent.__getitem__(self, key % N)
        elif isinstance(key, slice):
            start = key.start if key.start is not None else 0
            stop = key.stop if key.stop is not None else N
            step = 1 if key.step is None else key.step
            sim_start = self.index(self[start])
            if step > 0:
                direction = lambda x: x
                length = stop - start
            elif step < 0:
                direction = reversed
                length = start - stop
                step = abs(step)
                sim_start = N - sim_start - 1  # Reverse index
            else:
                raise ValueError("slice step cannot be zero")
            if length > 0:
                # Redifine start and stop with equivalent and simpler indexes.
                start = sim_start
                stop = sim_start + length
                out = []
                for i, elt in enumerate(cycle(direction(self))):
                    if i == stop:
                        return self._parent(out)
                    if (i - start) % step == 0 and i >= start:
                        out.append(elt)
            else:
                return self._parent()
        else:
            raise TypeError('{} indices must be integers or slices, '
                            'not {}'.format(self.__class__, type(key)))


class CyclicTuple(CyclicBase, tuple):
    _parent = tuple
    __doc__ = cyclic_doc.format(
        classname="CyclicTuple",
        classparent="tuple",
        A="(",
        Z=")",
        )


class CyclicList(CyclicBase, list):
    _parent = list
    __doc__ = (cyclic_doc + cyclic_doc_methods).format(
        classname="CyclicList",
        classparent="list",
        A="[",
        Z="]",
        )

    def turn(self, step=1):
        """
        foo.turn(step) -> None – change elements index of given step
        (move higher index to lower index with poisitive value).
        Equivalent to set at first position element at index 'step'.
        """
        try:
            step = int(step) % self.__len__()
        except ValueError:
            raise TypeError(
                "{} method 'turn' requires an integer but received a {}"
                .format(self.__class__.__name, type(step))
                )
        self._set_first_using_index(step)

    def set_first(self, elt):
        """
        foo.set_first(elt) -> None – set first occurence of 'elt' at first
        position.
        Raises ValueError if 'elt' is not present.
        """
        try:
            index = self.index(elt)
        except ValueError:
            raise ValueError("{} is not in CyclicList".format(elt))
        self._set_first_using_index(index)

    def _set_first_using_index(self, index):
        self.__init__(
            self._parent.__getitem__(self, slice(index, None, None))
            + self._parent.__getitem__(self, slice(None, index, None))
            )

###############################################################################


if __name__ == "__main__":

    import doctest

    doctest_result = doctest.testmod()
    print("\ndoctest >", doctest_result, "\n")


