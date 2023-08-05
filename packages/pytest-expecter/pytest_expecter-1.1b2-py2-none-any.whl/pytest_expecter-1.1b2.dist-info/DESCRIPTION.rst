pytest-expecter
===============

This is a fork of
`garybernhardt/expecter <https://github.com/garybernhardt/expecter>`__
that hides the internal stack trace for ``pytest``.

| |Build Status|
| |PyPI Version|

Overview
--------

This lets you write tests (using
`ropez/pytest-describe <https://github.com/ropez/pytest-describe>`__)
like this:

.. code:: python

    from expecter import expect


    def describe_foobar():

        def it_can_pass():
            expect(2 + 3) == 5

        def it_can_fail():
            expect(2 + 3) == 6

and instead of getting output like this:

.. code:: sh

    =================================== FAILURES ===================================
    _________________________ describe_foobar.it_can_fail __________________________

        def it_can_fail():
    >       expect(2 + 3) == 6

    test_foobar.py:14:
    _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

    self = expect(5), other = 6

        def __eq__(self, other):
            msg = 'Expected %s but got %s' % (repr(other), repr(self._actual))
            if (isinstance(other, basestring) and
                    isinstance(self._actual, basestring)):
                msg += normalized_diff(other, self._actual)
            elif len(repr(self._actual)) > 74:
                msg += normalized_diff(pprint.pformat(other),
                                       pprint.pformat(self._actual))
    >       assert self._actual == other, msg
    E       AssertionError: Expected 6 but got 5

    env/lib/python3.5/site-packages/expecter.py:57: AssertionError
    ====================== 1 failed, 1 passed in 2.67 seconds ======================

getting output like this:

.. code:: sh

    =================================== FAILURES ===================================
    _________________________ describe_foobar.it_can_fail __________________________

        def it_can_fail():
    >       expect(2 + 3) == 6
    E       AssertionError: Expected 6 but got 5

    test_foobar.py:14: AssertionError
    ====================== 1 failed, 1 passed in 2.67 seconds ======================

Installation
------------

.. code:: sh

    pip install pytest-expecter

.. |Build Status| image:: http://img.shields.io/travis/jacebrowning/pytest-expecter/plugin.svg
   :target: https://travis-ci.org/jacebrowning/pytest-expecter
.. |PyPI Version| image:: http://img.shields.io/pypi/v/pytest-expecter.svg
   :target: https://pypi.python.org/pypi/pytest-expecter

Revision History
================

1.1 (unreleased)
----------------

-  Add ``expect`` fixture to use directly in tests.

1.0 (2017/12/03)
----------------

-  Initial stable release.

0.2.2.post7 (2017/12/02)
------------------------

-  Added automatic conversion from ``OrderedDict`` to ``dict`` on Python
   3.6 to create readable diffs.


