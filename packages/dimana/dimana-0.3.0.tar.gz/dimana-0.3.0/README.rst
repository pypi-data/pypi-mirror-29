========================
_DIM_ensional _ANA_lysis
========================

A python library for tracking and verifying dimensional units of measure.

For background see the `dimensional analysis wikipedia entry`_.

.. _`dimensional analysis wikipedia entry`: https://en.wikipedia.org/wiki/Dimensional_analysis

.. contents::

A Tour of `dimana`
==================

Parsing Values
--------------

`dimana` values can be parsed with the ``Value`` constructor:

.. code:: python

   >>> from dimana import Value
   >>> reward = Value('12.5 [BTC]')
   >>> reward
   <Value '12.5 [BTC]'>

The grammar for units can handle powers expressed with the ``^`` symbol,
and a single division with the ``/`` symbol:

.. code:: python

   >>> Value('9.807 [meter/sec^2]')
   <Value '9.807 [meter / sec^2]'>

Arithmetic Operations
---------------------

Values track their units through arithmetic operations:

.. code:: python

   >>> time = Value('10 [min]')
   >>> rate = reward / time
   >>> rate
   <Value '1.25 [BTC / min]'>

Incoherent operations raise exceptions:

.. code:: python

   >>> reward + time # doctest: +IGNORE_EXCEPTION_DETAIL
   Traceback (most recent call last):
     ...
   UnitsMismatch: 'BTC' does not match 'min'

Value Components
----------------

A value associates a `scalar amount` with `dimensional units`. These
are available on the instance as ``amount`` and ``units``:

.. code:: python

   >>> rate.amount
   Decimal('1.25')
   >>> rate.units
   <Units 'BTC / min'>

Amounts
~~~~~~~

The scalar amount of a value is represented with ``decimal.Decimal``
instance on the ``amount`` attribute:

.. code:: python

   >>> reward.amount
   Decimal('12.5')

Arithmetic operations rely on the `decimal` library for arithmetic logic,
including precision tracking:

.. code:: python

   >>> reward * Value('713.078000 [USD / BTC]')
   <Value '8913.4750000 [USD]'>

Units
~~~~~

Units are available in the ``units`` attribute of ``Value``
instances. They are instances of ``dimana.Units``. You can parse ``Units``
instances directly:

.. code:: python

   >>> from dimana import Units
   >>> meter = Units('meter')
   >>> meter
   <Units 'meter'>
   >>> sec = Units('sec')
   >>> sec
   <Units 'sec'>

Constructing Values
-------------------

There are four ways to create values:

* parsing a 'value text' with the constructor: ``Value``,
* as the result of arithmetic operations on other values,
* with the `explicit constructor`,
* by calling a ``Units`` instance.

The first two are described above, the last two next:

Explicit Value Constructor
~~~~~~~~~~~~~~~~~~~~~~~~~~

Values can be constructed explicitly directly given ``Decimal`` and ``Units`` instances:

.. code:: python

   >>> from dimana import Value
   >>> from decimal import Decimal
   >>> Value(Decimal('23.50'), meter)
   <Value '23.50 [meter]'>

Note that this constructor is strict about types and the first argument *must* be a ``decimal.Decimal``:

.. code:: python

   >>> Value(7, meter)
   Traceback (most recent call last):
     ...
   TypeError: Expected 'Decimal', found 'int'

Calling Units
~~~~~~~~~~~~~

Many applications require a finite statically known set of ``Units``
instances, and then need to create ``Value`` instances from specific
explicit ``Units`` instances. This is more specific (thus safer) when
the units are already known than calling the ``Value`` constructor which
returns a value with arbitrary units.

For example:

.. code:: python

   >>> from decimal import Decimal
   >>> from dimana import Value, Units
   >>> METER = Units('METER')
   >>> userinput = '163' # In an application this might be from arbitrary input.
   >>> height = Value(Decimal(userinput), METER)
   >>> height
   <Value '163 [METER]'>

Because this pattern is so common, ``Units`` instances support parsing
an amount directly by calling ``Units`` instances:

.. code:: python

   >>> height2 = METER(userinput)
   >>> height == height2
   True

str() and repr()
----------------

The ``str()``\ -ification of ``Value`` and ``Units`` instances matches the
'canonical parsing format':

.. code:: python

   >>> trolls = Value('3 [troll]')
   >>> print(trolls)
   3 [troll]
   >>> trolls == Value(str(trolls))
   True

The ``repr()`` of these class instances contains the class name and the
``str()``\ -ification:

.. code:: python

   >>> print(repr(trolls))
   <Value '3 [troll]'>
   >>> print(repr(trolls.units))
   <Units 'troll'>

More About Units
----------------

This section explores the ``Units`` class more closely.

``zero`` and ``one``
~~~~~~~~~~~~~~~~~~~~

Because the 0 and 1 amounts are very common, they are available as
attributes of a ``Units`` instance:

.. code:: python

   >>> meter.zero
   <Value '0 [meter]'>
   >>> sec.one
   <Value '1 [sec]'>

Scalar Units
~~~~~~~~~~~~

The base case of units with 'no dimension' is available as
``Scalar``. This instance of ``Units`` represents, for example,
ratios:

.. code:: python

   >>> from dimana import Scalar
   >>> total = Value('125 [meter]')
   >>> current = Value('15 [meter]')
   >>> completion = current / total
   >>> completion
   <Value '0.12'>
   >>> completion.units is Scalar
   True

Parsing a value which does not specify units produces a scalar value:

.. code:: python

   >>> completion == Value('0.12')
   True

By design, `dimana` does not do implicit coercion of `float` instances
into `Value` instances to help avoid numeric bugs:

.. code:: python

   >>> experience = Value('42 [XP]')
   >>> experience * 1.25
   Traceback (most recent call last):
     ...
   TypeError: Expected 'Value', found 'float'

Using ``Scalar`` is necessary in these cases. Parsing
a value with no units specification gives a 'scalar value':

.. code:: python

   >>> experience * Value('1.25')
   <Value '52.50 [XP]'>

Units Uniqueness and Matching
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There is a single instance of ``Units`` for each combination of unit:

.. code:: python

   >>> (meter + meter) is meter
   True
   >>> (meter / sec) is Units('meter / sec')
   True

Thus, to test if two ``Units`` instances represent the same units,
just use the ``is`` operator:

.. code:: python

   >>> if meter is (Units('meter / sec') * sec):
   ...     print('Yes, it is meters.')
   ...
   Yes, it is meters.

The ``Units.match`` method does such a check and raises ``UnitsMismatch``
if the units do not match:

.. code:: python

   >>> meter.match(Units('meter / sec') * sec)
   >>> meter.match(Units('meter / sec^2') * sec) # doctest: +IGNORE_EXCEPTION_DETAIL
   Traceback (most recent call last):
     ...
   UnitsMismatch: 'meter' does not match 'meter / sec'

Uniqueness Implications
+++++++++++++++++++++++

This uniqueness depends globally on the unit string names, so if a large
application depended on two completely separate libraries, each of which
rely on `dimana`, and both libraries define ``<Units 's'>`` they will
be using the same instance. This could be a problem if, for example,
one library uses the ``S`` to represent `seconds` while the other uses
it to represent `Siemens <https://en.wikipedia.org/wiki/Siemens_(unit)>`_.

Each instance of ``Units`` persists to the end of the process, so
instantiating ``Units`` dynamically could present a resource management
problem, especially if a malicious entity can instantiate arbitrary
unit types.

(The plan is to wait for real life applications that encounter these
problems before adding complexity to this package.)


Past, Present, and Future
=========================

Future
------

There is no definite roadmap other than to adapt to existing users'
needs. However, some potential new features would be:

- Python 3 support with an identical API.
- Support for more numeric operations.
- More streamlined interaction with ``decimal``, such as for rounding a
  ``Value`` to a given precision.
- Add an 'expression evaluator' for quick-and-easy interactive interpreter
  calculations, eg: ``dimana.eval``
- Add a commandline wrapper around ``eval``.

Changelog
---------

0.3
~~~

- Removed old class-scoped APIs, such as `parse` methods, in favor of
  using constructors directly.
- Added tox support for python 2.7 and 3.5.

0.2.1
~~~~~

- Extended the README.rst to have a more complete overview, a future
  roadmap, and this changelog.
- Made several breaking API changes:

  + Now toplevel ``dimana`` only publicly exposes ``Units`` and ``Value``.
  + Introduced ``Units.from_string`` parser.
  + Introduced ``zero`` and ``one`` properties of ``Units`` instances.
  + Renamed the old ``Value.decimal`` attribute to ``Value.amount``.

0.2.0
~~~~~

- Added code examples in README.rst and hooked doctests of that
  documentation into the unittest suite.
- Pivoted the API to the separation between ``Value`` and ``Units``
  with the two ``parse`` methods.
- Strict requirement of ``Decimal`` instances without implicit coercion.

Before 0.2.0
~~~~~~~~~~~~

The 0.1 line of `dimana` had a very different interface based on a
single `Dimana` class, and a more rudimentary parser, and was generally
a messier proof-of-concept.

- There was no representation of the modern ``Units`` instances, rather
  only the equivalent of ``Value`` instances.
- It used dynamic type generation for what is now each instance of
  ``Units``.
- It had less obvious error messages and less complete unit testing.
- It had no documentation and no doctests.

About This Document
===================

There appears to be no way to accurately test exception details with doctest for both python 2 and 3. The `best option <https://stackoverflow.com/questions/17671147/how-to-test-exceptions-with-doctest-in-python-2-x-and-3-x>`_ seems to be to ignore exception details. :-<
