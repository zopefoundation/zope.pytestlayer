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


class BarLayer:

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


class FooBarLayer(FooLayer, BarLayer):

    @classmethod
    def setUp(cls):
        cls.layer_foobar = 'layer foobar'

    @classmethod
    def tearDown(cls):
        del cls.layer_foobar

    @classmethod
    def testSetUp(cls):
        log_to_terminal(cls.pytest_request, 'testSetUp foobar')
        cls.test_foobar = 'test foobar'

    @classmethod
    def testTearDown(cls):
        log_to_terminal(cls.pytest_request, 'testTearDown foobar')
        del cls.test_foobar


class FooTest(unittest.TestCase):

    layer = FooLayer

    def test_dummy(self):
        self.assertEqual('layer foo', self.layer.layer_foo)
        self.assertEqual('test foo', self.layer.test_foo)
        self.assertFalse(hasattr(self.layer, 'layer_bar'))
        self.assertFalse(hasattr(self.layer, 'test_bar'))


class BarTest(unittest.TestCase):

    layer = BarLayer

    def test_dummy(self):
        self.assertFalse(hasattr(self.layer, 'layer_foo'))
        self.assertFalse(hasattr(self.layer, 'test_foo'))
        self.assertEqual('layer bar', self.layer.layer_bar)
        self.assertEqual('test bar', self.layer.test_bar)


class FooBarTest(unittest.TestCase):

    layer = FooBarLayer

    def test_dummy(self):
        self.assertEqual('layer foo', self.layer.layer_foo)
        self.assertEqual('test foo', self.layer.test_foo)
        self.assertEqual('layer bar', self.layer.layer_bar)
        self.assertEqual('test bar', self.layer.test_bar)
        self.assertEqual('layer foobar', self.layer.layer_foobar)
        self.assertEqual('test foobar', self.layer.test_foobar)


class Bar2Test(unittest.TestCase):

    layer = BarLayer

    def test_dummy(self):
        self.assertFalse(hasattr(self.layer, 'layer_foo'))
        self.assertFalse(hasattr(self.layer, 'test_foo'))
        self.assertEqual('layer bar', self.layer.layer_bar)
        self.assertEqual('test bar', self.layer.test_bar)


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
                'foobar.txt',
                optionflags=OPTIONFLAGS,
            ),
            layer=FooBarLayer,
        ),
    ])
    return suite
