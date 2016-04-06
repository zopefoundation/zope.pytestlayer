===================================
The gocept.pytestlayer distribution
===================================

Integration of zope.testrunner-style test layers into the `py.test`_
framework

This package is compatible with Python versions 2.6 and 2.7. (To run its tests
successfully you should use at least Python 2.7.4 because of a bug in earlier
Python 2.7 versions.)

.. _`py.test` : http://pytest.org

Quick start
===========

* Make sure your test files follow the `conventions of py.test's test
  discovery`_

  .. _`conventions of py.test's test discovery`:
     http://pytest.org/latest/goodpractises.html#python-test-discovery

  In particular, a file named ``tests.py`` will not be recognised.

* Add a buildout section to create the `py.test` runner::

    [buildout]
    parts += pytest

    [pytest]
    recipe = zc.recipe.egg
    eggs = gocept.pytestlayer
           pytest
           <YOUR PACKAGE HERE>

``gocept.pytestlayer`` registers itself as a ``py.test`` plugin. This way, nothing
more is needed to run an existing Zope or Plone test suite.


Not supported use cases
=======================

* Inheriting from a base class while changing the layer. See `issue #5`_

* Mixing classes inheriting ``unittest.TestCase`` and a ``test_suite()`` function (e. g. to create a ``DocTestSuite`` or a ``DocFileSuite``) in a single module (aka file).

  * This is a limitation of the `py.test` test discovery which ignores the doctests in this case.

  * Solution: Put the classes and ``test_suite()`` into different modules.

* A ``doctest.DocFileSuite`` which does not have a ``layer`` is silently skipped. Use the built-in doctest abilities of py.test to run those tests.

.. _`issue #5` : https://bitbucket.org/gocept/gocept.pytestlayer/issues/5