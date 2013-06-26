Welcome to python-rex
=====================

.. image:: https://pypip.in/v/python-rex/badge.png
   :target: https://crate.io/packages/python-rex
.. image:: https://pypip.in/d/python-rex/badge.png
   :target: https://crate.io/packages/python-rex
.. image:: https://travis-ci.org/cypreess/python-rex.png?branch=master
   :target: https://travis-ci.org/cypreess/python-rex
.. image:: https://coveralls.io/repos/cypreess/python-rex/badge.png?branch=master
   :target: https://coveralls.io/r/cypreess/python-rex?branch=master
   
Python **rex** is regular expressions for humans. (**rex** is also abbreviation from **re** **X** tended).

It is for the `re standard module <http://docs.python.org/2/library/index.html>`_ like
`requests <http://docs.python-requests.org/en/latest/>`_ is for `urllib module <http://docs.python.org/2/library/urllib.html>`_.

**Rex** also is `latin for "king" <http://en.wikipedia.org/wiki/Rex>`_, and the king of regular expressions is Perl. 
So **rex** API tries to mimic at least some Perl's idioms.

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

So far **rex** supports:

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

