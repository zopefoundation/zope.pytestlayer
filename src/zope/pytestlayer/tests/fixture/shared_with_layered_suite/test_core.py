import doctest
import unittest

from plone.testing import layered

from zope.pytestlayer.testing import log_to_terminal


class FooLayer(object):

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


class FooTest(unittest.TestCase):

    layer = FooLayer

    def test_dummy(self):
        self.assertEqual('layer foo', self.layer.layer_foo)
        self.assertEqual('test foo', self.layer.test_foo)


def test_suite():
    suite = unittest.TestSuite()

    OPTIONFLAGS = (doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)

    suite.addTests([
        layered(
            doctest.DocFileSuite(
                'mydoctest.txt',
                optionflags=OPTIONFLAGS,
            ),
            layer=FooLayer,
        ),
    ])
    return suite
