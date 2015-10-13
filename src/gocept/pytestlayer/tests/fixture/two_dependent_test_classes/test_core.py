import unittest
from gocept.pytestlayer.testing import log_to_terminal


class Layer(object):

    def __init__(self, name):
        self.name = name
        self.__bases__ = []

    def setUp(self):
        self.layer_val = 'layer {0.name}'.format(self)

    def tearDown(self):
        del self.layer_val

    def testSetUp(self):
        log_to_terminal(self.pytest_request, 'testSetUp {0.name}'.format(self))
        self.test_val = 'test {0.name}'.format(self)

    def testTearDown(self):
        log_to_terminal(
            self.pytest_request, 'testTearDown {0.name}'.format(self))
        del self.test_val

FooLayer = Layer('foo')
BarLayer = Layer('bar')


class FooTest(unittest.TestCase):

    layer = FooLayer
    name = 'foo'

    def test_dummy(self):
        self.assertEqual('layer {0.name}'.format(self), self.layer.layer_val)
        self.assertEqual('test {0.name}'.format(self), self.layer.test_val)


class BarTest(FooTest):

    layer = BarLayer
    name = 'bar'

    def test_dummy2(self):
        self.assertEqual('layer {0.name}'.format(self), self.layer.layer_val)
        self.assertEqual('test {0.name}'.format(self), self.layer.test_val)
