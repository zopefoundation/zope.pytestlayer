===================================
The gocept.pytestlayer distribution
===================================

.. image:: https://img.shields.io/pypi/v/gocept.pytestlayer.svg
    :target: https://pypi.org/project/gocept.pytestlayer/

.. image:: https://img.shields.io/pypi/pyversions/gocept.pytestlayer.svg
    :target: https://pypi.org/project/gocept.pytestlayer/

.. image:: https://github.com/gocept/gocept.pytestlayer/workflows/tests/badge.svg
    :target: https://github.com/gocept/gocept.pytestlayer/actions?query=workflow%3Atests

.. image:: https://coveralls.io/repos/github/gocept/gocept.pytestlayer/badge.svg?branch=main
    :target: https://coveralls.io/github/gocept/gocept.pytestlayer?branch=main


Integration of zope.testrunner-style test layers into the `pytest`_
framework

This package is compatible with Python versions 3.7 - 3.10 including
PyPy3.

.. _`pytest` : http://pytest.org

Quick start
===========

* Make sure your test files follow the `conventions of pytest's test
  discovery`_

  .. _`conventions of pytest's test discovery`:
     http://pytest.org/latest/goodpractises.html#python-test-discovery

  In particular, a file named ``tests.py`` will not be recognised.

* Add a buildout section to create the `pytest` runner::

    [buildout]
    parts += pytest

    [pytest]
    recipe = zc.recipe.egg
    eggs = gocept.pytestlayer
           pytest
           <YOUR PACKAGE HERE>

``gocept.pytestlayer`` registers itself as a ``pytest`` plugin. This way, nothing
more is needed to run an existing Zope or Plone test suite.

Advanced usage
==============

Version 2.1 reintroduced `fixture.create()` to be able to define the name of the generated to pytest fixtures. So it is possible to use them in function style tests.

Example (Code has to be in `contest.py`!)::

    from .testing import FUNCTIONAL_LAYER
    import gocept.pytestlayer.fixture

    globals().update(gocept.pytestlayer.fixture.create(
        FUNCTIONAL_LAYER,
        session_fixture_name='functional_session',
        class_fixture_name='functional_class',
        function_fixture_name='functional'))

This creates three fixtures with the given names and the scopes in the argument name. The session and class fixtures run `setUp()` and `tearDown()` of the layer if it has not been run before while the function fixture runs `testSetUp()` and `testTearDown()` of the layer. The function fixture depends on the session one. The fixtures return the instance of the layer. So you can use the `functional` fixture like this::

    def test_mymodule__my_function__1(functional):
        assert functional['app'] is not None

Not supported use cases
=======================

* Inheriting from a base class while changing the layer. See commit `f879f9e <https://github.com/gocept/gocept.pytestlayer/commit/f879f9eb21cbd41a843b5021bc1264e9462fb505>`_.

* Mixing classes inheriting ``unittest.TestCase`` and a ``test_suite()`` function (e. g. to create a ``DocTestSuite`` or a ``DocFileSuite``) in a single module (aka file).

  * This is a limitation of the `pytest` test discovery which ignores the doctests in this case.

  * Solution: Put the classes and ``test_suite()`` into different modules.

* A ``doctest.DocFileSuite`` which does not have a ``layer`` is silently skipped. Use the built-in doctest abilities of pytest to run those tests.
