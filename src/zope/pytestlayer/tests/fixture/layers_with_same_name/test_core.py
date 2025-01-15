import unittest


class Layer:

    def __init__(self, value, bases=()):
        self.__name__ = 'TestLayer'
        self.__bases__ = bases
        self.value = value

    def setUp(self):
        self.set_up_value = self.value

    def tearDown(self):
        del self.set_up_value


FooLayer = Layer('foo-layer')
BarLayer = Layer('bar-layer')
FooBarLayer = Layer('foobar-layer', bases=(FooLayer, BarLayer))


class FooTest(unittest.TestCase):

    layer = FooLayer

    def test_dummy(self):
        self.assertEqual('foo-layer', self.layer.set_up_value)


class BarTest(unittest.TestCase):

    layer = BarLayer

    def test_dummy(self):
        self.assertEqual('bar-layer', self.layer.set_up_value)


del FooLayer
del BarLayer
