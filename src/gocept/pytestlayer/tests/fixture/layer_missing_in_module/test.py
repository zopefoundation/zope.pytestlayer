import logging
import unittest

log = logging.getLogger('zopelayer')
log.addHandler(logging.StreamHandler())


class FooLayer(object):
    __name__ = 'FooLayer'


class FooTest(unittest.TestCase):

    layer = FooLayer()

    def test_dummy(self):
        self.assertEqual(1, 1)
