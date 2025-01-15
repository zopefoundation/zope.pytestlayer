import unittest


class FooLayer:
    pass


class FooTest(unittest.TestCase):

    layer = FooLayer

    def test_dummy(self):
        self.assertFalse(hasattr(self.layer, 'layer_foo'))
        self.assertFalse(hasattr(self.layer, 'test_foo'))
