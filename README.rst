Welcome to python-Rex
=====================

.. image:: https://pypip.in/v/python-rex/badge.png
   :target: https://crate.io/packages/python-rex
.. image:: https://pypip.in/d/python-rex/badge.png
   :target: https://crate.io/packages/python-rex
.. image:: https://travis-ci.org/cypreess/python-rex.png?branch=master
   :target: https://travis-ci.org/cypreess/python-rex
.. image:: https://coveralls.io/repos/cypreess/python-rex/badge.png?branch=master
   :target: https://coveralls.io/r/cypreess/python-rex?branch=master
   
Python **Rex** is regular expressions for humans. (**Rex** is also abbreviation from **re** **X** tended).

**Rex** is for the `re standard module <http://docs.python.org/2/library/index.html>`_ as
`requests <http://docs.python-requests.org/en/latest/>`_ is for `urllib module <http://docs.python.org/2/library/urllib.html>`_.

**Rex** also is `latin for "king" <http://en.wikipedia.org/wiki/Rex>`_, and the king of regular expressions is Perl.
So **Rex** API tries to mimic at least some Perl's idioms.

Installation
============

::

    pip install python-rex

or

::
   
   pip install -e git+https://github.com/cypreess/python-rex.git#egg=rex-dev

There are no external dependencies. 


::
   
   from rex import rex



Quickstart
==========

Do that::

   from rex import rex
   print ("Your ticket number: XyZ-1047. Have fun!" == rex("/[a-z]{3}-(\d{4})/i"))[1]
    

instead of doing that::

   import re
   regex = re.compile("[a-z]{3}-(\d{4})", flags=re.IGNORECASE)
   m = regex.search("Your ticket number: XyZ-1047. Have fun!")
   
   if m is not None:
      print m.group(1)
   else:
      print None
   
   # or in shorter way
   print m.group(1) if m else None


(both should print ``1047``).

Docs
====

So far **Rex** supports:

* simple matching (first match),
* substitution,
* all python re flags.



Matching 
--------

The most obvious usage - test condition by matching to string::

    if 'This is a dog' == rex('/dog/'):
        print 'Oh yeah'


or::

    if 'My lucky 777 number' == rex('/[0-9]+/'):
        print 'Number found'


You can use Perl notation and prepend ``m`` character to your search::


    if 'My lucky 777 number' == rex('m/[0-9]+/'):
        print 'Number found'


but you can also simply check your match::


    if ('My lucky 777 number' == rex('m/[0-9]+/'))[0] == '777':
        print 'Number found'

or even groups::


    if ('My lucky 777 number' == rex('m/(?P<number>[0-9]+)/'))['number'] == '777':
        print 'Number found'


Remember a mess with re module when it does not match anything? Rex won't let you down,
it will kindly return ``None`` for whatever you ask::

    >>> print ('My lucky 777 number' == rex('m/(?P<number>[0-9]+)/'))['no_such_group']
    None

    >>> print ("I don't tell you my lucky number" == rex('m/(?P<number>[0-9]+)/'))['number']
    None


Substituting
------------

Substitution can be made by prefixing pattern with ``s`` character (like in perl expression)::

    >>> print "This is a cat" == rex('s/CAT/dog/i')
    This is a dog


Flags
-----

Every **Rex** pattern as in Perl patterns allows to suffix some flags, e.g. ``rex('/pattern/iu')`` for enabling ``i`` and ``u`` flag. **Rex** supports all standard python re flags:

* ``d`` - re.DEBUG
* ``i`` - re.IGNORECASE
* ``l`` - re.LOCALE
* ``m`` - re.MULTILINE
* ``s`` - re.DOTALL
* ``u`` - re.UNICODE
* ``x`` - re.VERBOSE

Caching
-------

**Rex** caches all patterns so reusing patterns is super fast. You can always clear **Rex** cache by calling ``rex_clear_cache()`` or
disable caching for specific patterns ``rex('/pattern/', cache=False)``.


Rex for orthodox
----------------

If you are so orthodox pythonist that couldn't leave with overloaded ``==`` operator syntax in your codebase,
you can use "orthodox mode" of rex. Just put the string to match/substitute against as a second argument::

    >>> bool(rex("/dog/", "This is a dog"))
    True
    >>> rex("s/cat/dog/", "This is a cat")
    'This is a dog'



