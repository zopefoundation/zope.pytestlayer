import unittest

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
