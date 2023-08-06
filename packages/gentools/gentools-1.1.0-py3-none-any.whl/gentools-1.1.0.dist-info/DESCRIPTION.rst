Gentools
========

.. image:: https://img.shields.io/pypi/v/gentools.svg?style=flat-square
    :target: https://pypi.python.org/pypi/gentools

.. image:: https://img.shields.io/pypi/l/gentools.svg?style=flat-square
    :target: https://pypi.python.org/pypi/gentools

.. image:: https://img.shields.io/pypi/pyversions/gentools.svg?style=flat-square
    :target: https://pypi.python.org/pypi/gentools

.. image:: https://img.shields.io/travis/ariebovenberg/gentools.svg?style=flat-square
    :target: https://travis-ci.org/ariebovenberg/gentools

.. image:: https://img.shields.io/codecov/c/github/ariebovenberg/gentools.svg?style=flat-square
    :target: https://coveralls.io/github/ariebovenberg/gentools?branch=master

.. image:: https://img.shields.io/readthedocs/gentools.svg?style=flat-square
    :target: http://gentools.readthedocs.io/en/latest/?badge=latest

.. image:: https://img.shields.io/codeclimate/maintainability/ariebovenberg/gentools.svg?style=flat-square
    :target: https://codeclimate.com/github/ariebovenberg/gentools/maintainability


Tools for generators, generator functions, and generator-based coroutines.

Key features:

* Create reusable generators
* Compose generators
* Build python 2/3-compatible generators with ``return``.

Installation
------------

.. code-block:: bash

   pip install gentools

Examples
--------

- Make generator functions reusable:

.. code-block:: python

   >>> @reusable
   ... def countdown(value, step):
   ...     while value > 0:
   ...         yield value
   ...         value -= step

   >>> from_3 = countdown(3, step=1)
   >>> list(from_3)
   [3, 2, 1]
   >>> list(from_3)
   [3, 2, 1]
   >>> isinstance(from_3, countdown)  # generator func is wrapped in a class
   True
   >>> from_3.step  # attribute access to arguments
   1
   >>> from_3.replace(value=5)  # create new instance with replaced fields
   countdown(value=5, step=1)  # descriptive repr()

- map a generator's ``yield``, ``send``, and ``return`` values:

.. code-block:: python

   >>> @map_return('final value: {}'.format)
   ... @map_send(int)
   ... @map_yield('the current max is: {}'.format)
   ... def my_max(value):
   ...     while value < 100:
   ...         newvalue = yield value
   ...         if newvalue > value:
   ...             value = newvalue
   ...     return value

   >>> gen = my_max(5)
   >>> next(gen)
   'the current max is: 5'
   >>> gen.send(11.3)
   'the current max is: 11'
   >>> gen.send(104)
   StopIteration('final value: 104')

- relay a generator's yield/send interactions through another generator:

.. code-block:: python

   >>> def try_until_positive(outvalue):
   ...     value = yield outvalue
   ...     while value < 0:
   ...         value = yield 'not positive, try again'
   ...     return value

   >>> @relay(try_until_positive)
   ... def my_max(value):
   ...     while value < 100:
   ...         newvalue = yield value
   ...         if newvalue > value:
   ...             value = newvalue
   ...     return value

   >>> gen = my_max(5)
   >>> next(gen)
   5
   >>> gen.send(-4)
   'not positive, try again'
   >>> gen.send(-1)
   'not positive, try again'
   >>> gen.send(8)
   8
   >>> gen.send(104)
   StopIteration(104)

- make python 2/3 compatible generators with ``return``.

.. code-block:: python

   >>> @py2_compatible
   ... def my_max(value):
   ...     while value < 100:
   ...         newvalue = yield value
   ...         if newvalue > value:
   ...             value = newvalue
   ...     return_(value)


Release history
---------------

development
+++++++++++

1.1.0 (2018-03-02)
++++++++++++++++++

- added support for python 2.7, 3.3
- new ``py2_compatible`` decorator with py2/3 compatible ``return_``
- new ``stopiter_value`` helper
- improvements to documentation

1.0.2 (2018-02-08)
++++++++++++++++++

- add more examples to docs

1.0.1 (2018-01-27)
++++++++++++++++++

- update dev status classifier

1.0.0 (2018-01-27)
++++++++++++++++++

- Include ``compose`` in public API

0.4.0 (2018-01-24)
++++++++++++++++++

- rename ``pipe`` to ``relay``.

0.3.1 (2018-01-23)
++++++++++++++++++

- fix copy issue in reusable generator ``.replace()``

0.3.0 (2018-01-22)
++++++++++++++++++

- make reusable generators callable as methods

0.2.2 (2018-01-21)
++++++++++++++++++

- updates to readme

0.2.0 (2018-01-21)
++++++++++++++++++

- reorganized modules, improved docs, renamed functions.

0.1.0 (2018-01-17)
++++++++++++++++++

- initial release


