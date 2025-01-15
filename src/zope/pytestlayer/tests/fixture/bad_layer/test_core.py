import unittest


class FooLayer:
    __name__ = 'FooLayer'


class FooTest(unittest.TestCase):

    layer = FooLayer()

    def test_dummy(self):
        self.assertEqual(1, 1)
