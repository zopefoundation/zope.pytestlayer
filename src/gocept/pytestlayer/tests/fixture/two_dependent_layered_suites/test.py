import unittest
import doctest
from plone.testing import layered
from gocept.pytestlayer.testing import log_to_terminal


class FooLayer(object):

    @classmethod
    def setUp(cls):
        cls.layer_foo = 'layer foo'

    @classmethod
    def tearDown(cls):
        del cls.layer_foo

    @classmethod
    def testSetUp(cls):
        log_to_terminal(cls.pytest_request, '\ntestSetUp foo')
        cls.test_foo = 'test foo'

    @classmethod
    def testTearDown(cls):
        log_to_terminal(cls.pytest_request, '\ntestTearDown foo')
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
        log_to_terminal(cls.pytest_request, '\ntestSetUp bar')
        cls.test_bar = 'test bar'

    @classmethod
    def testTearDown(cls):
        log_to_terminal(cls.pytest_request, '\ntestTearDown bar')
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
