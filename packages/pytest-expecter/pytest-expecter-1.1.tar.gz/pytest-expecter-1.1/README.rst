pytest-expecter
===============

A ``pytest`` plugin for
`garybernhardt/expecter <https://github.com/garybernhardt/expecter>`__
that hides the internal stacktrace.

| |Build Status|
| |PyPI Version|

Overview
--------

This lets you write tests (optionally using
`ropez/pytest-describe <https://github.com/ropez/pytest-describe>`__)
like this:

.. code:: python

    def describe_foobar():

        def it_can_pass(expect):
            expect(2 + 3) == 5

        def it_can_fail(expect):
            expect(2 + 3) == 6

and get output like this:

.. code:: sh

    =================================== FAILURES ===================================
    _________________________ describe_foobar.it_can_fail __________________________

        def it_can_fail(expect):
    >       expect(2 + 3) == 6
    E       AssertionError: Expected 6 but got 5

    test_foobar.py:7: AssertionError
    ====================== 1 failed, 1 passed in 2.67 seconds ======================

Installation
------------

.. code:: sh

    pip install pytest-expecter

.. |Build Status| image:: http://img.shields.io/travis/jacebrowning/pytest-expecter/plugin.svg
   :target: https://travis-ci.org/jacebrowning/pytest-expecter
.. |PyPI Version| image:: http://img.shields.io/pypi/v/pytest-expecter.svg
   :target: https://pypi.python.org/pypi/pytest-expecter
