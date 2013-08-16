===================================
The gocept.pytestlayer distribution
===================================

Integration of zope.testrunner-style test layers into the py.test framework

This package is compatible with Python version 2.7.


Quick start
===========

* Write a `conftest.py` creating fixtures for your layers::

    from gocept.pytestlayer.fixture import create
    from .testing import Layer1, Layer2

    pytest_plugins = ('zopelayer')
    globals().update(create(Layer1, Layer2))

* Add a buildout section to create the py.test runner::

    [buildout]
    parts += pytest

    [pytest]
    recipe = zc.recipe.egg
    eggs = gocept.pytestlayer
           pytest
           <YOUR PACKAGE HERE>
