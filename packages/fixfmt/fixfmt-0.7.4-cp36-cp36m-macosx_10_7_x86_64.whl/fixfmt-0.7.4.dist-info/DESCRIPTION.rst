
A C++ and Python library for formatting values (numbers, strings, etc.)
in fixed-width fields. Useful for printing tabular data and similar.

For example, strings:

.. code:: py

    >>> fmt = fixfmt.String(10)
    >>> fmt("testing")
    'testing   '
    >>> fmt("Hello, world!")
    'Hello, wo…'

and numbers:

.. code:: py

    >>> fmt = fixfmt.Number(3, 3)
    >>> fmt(math.pi)
    '   3.142'

Includes C++ and Python libraries.  Requires a C++14 compiler and GNU Make to
build.


