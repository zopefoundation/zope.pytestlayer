===================================
The gocept.pytestlayer distribution
===================================

Integration of zope.testrunner-style test layers into the `py.test`_
framework

This package is compatible with Python version 2.7. (To run its tests
successfully you sould use at lest Python 2.7.4 because of a bug in earlier
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

`gocept.pytestlayer` registers itself as a `py.test` plugin. This way, nothing
more is needed to run an existing Zope or Plone test suite.
