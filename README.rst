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

* Write a ``conftest.py`` to explicitely use the plugin::
    
    pytest_plugins = ('zopelayer', )

  Make sure to put the ``conftest.py`` inside a directory that is a parent of
  all directories that contain tests that use layers, so it is found by pytest
  whenever needed.
