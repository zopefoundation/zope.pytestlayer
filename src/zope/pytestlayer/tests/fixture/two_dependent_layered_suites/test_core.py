import doctest
import unittest

from plone.testing import layered

from zope.pytestlayer.testing import log_to_terminal


class FooLayer:

    @classmethod
    def setUp(cls):
        cls.layer_foo = 'layer foo'

    @classmethod
    def tearDown(cls):
        del cls.layer_foo

    @classmethod
    def testSetUp(cls):
        log_to_terminal(cls.pytest_request, 'testSetUp foo')
        cls.test_foo = 'test foo'

    @classmethod
    def testTearDown(cls):
        log_to_terminal(cls.pytest_request, 'testTearDown foo')
        del cls.test_foo


class BarLayer(FooLayer):

    @classmethod
    def setUp(cls):
        cls.layer_bar = 'layer bar'

    @classmethod
    def tearDown(cls):
        del cls.layer_bar

    @classmethod
    def testSetUp(cls):
        log_to_terminal(cls.pytest_request, 'testSetUp bar')
        cls.test_bar = 'test bar'

    @classmethod
    def testTearDown(cls):
        log_to_terminal(cls.pytest_request, 'testTearDown bar')
        del cls.test_bar


def test_suite():
    suite = unittest.TestSuite()

    OPTIONFLAGS = (doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)

    suite.addTests([
        layered(
            doctest.DocFileSuite(
                'foo.txt',
                optionflags=OPTIONFLAGS,
            ),
            layer=FooLayer,
        ),
        layered(
            doctest.DocFileSuite(
                'bar.txt',
                optionflags=OPTIONFLAGS,
            ),
            layer=BarLayer,
        ),
    ])
    return suite
