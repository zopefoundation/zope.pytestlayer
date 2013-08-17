===================================
The gocept.pytestlayer distribution
===================================

Integration of zope.testrunner-style test layers into the `py.test`_
framework

This package is compatible with Python version 2.7.

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

* Write a ``conftest.py`` creating fixtures for your layers::

    from gocept.pytestlayer import fixture

    globals().update(fixture.create(
        "mypackage.testing.Layer1",
        "mypackage.testing.Layer2",
        ))

  As long as there are any fixtures missing, the plugin will tell you about
  layers that need to be included. Calling ``py.test -x`` will make this
  process faster (as it makes the runner stop at the first error).

  Make sure to put the ``conftest.py`` inside a directory that is a parent of
  all directories that contain tests that use layers, so it is found by pytest
  whenever needed.
