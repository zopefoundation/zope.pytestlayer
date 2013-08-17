import logging
import unittest

log = logging.getLogger('zopelayer')
log.addHandler(logging.StreamHandler())


class FooLayer(object):
    pass


class FooTest(unittest.TestCase):

    layer = FooLayer

    def test_dummy(self):
        self.assertFalse(hasattr(self.layer, 'layer_foo'))
        self.assertFalse(hasattr(self.layer, 'test_foo'))
